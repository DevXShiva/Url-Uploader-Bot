import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import asyncio
import aiohttp
import json
import math
import os
import shutil
import time
from datetime import datetime
from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
from plugins.database.database import db
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import enums 

async def ddl_call_back(bot, update):
    logger.info(update)
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")
    
    youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = os.path.basename(youtube_dl_url)
    
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0].strip()
            custom_file_name = url_parts[1].strip()
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]

    if youtube_dl_url is not None:
        youtube_dl_url = youtube_dl_url.strip()
    if custom_file_name is not None:
        custom_file_name = custom_file_name.strip()

    # Task ID for Cancel Logic
    task_id = str(update.message.id)
    if task_id not in Config.DOWNLOAD_LOCATION:
        Config.DOWNLOAD_LOCATION.append(task_id)

    description = Translation.CUSTOM_CAPTION_UL_FILE
    start = datetime.now()
    
    await update.message.edit_caption(
        caption=Translation.DOWNLOAD_START,
        parse_mode=enums.ParseMode.HTML
    )

    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION[0] + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name

    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            # Added task_id for cancellation support
            download_status = await download_coroutine(
                bot, session, youtube_dl_url, download_directory,
                update.message.chat.id, update.message.id, c_time, task_id
            )
            if download_status is False:
                return False
        except asyncio.TimeoutError:
            await bot.edit_message_text(
                text=Translation.SLOW_URL_DECED,
                chat_id=update.message.chat.id,
                message_id=update.message.id
            )
            return False

    if os.path.exists(download_directory):
        end_one = datetime.now()
        await update.message.edit_caption(
            caption=Translation.UPLOAD_START,
            parse_mode=enums.ParseMode.HTML
        )
        
        file_size = os.stat(download_directory).st_size
        if file_size > Config.TG_MAX_FILE_SIZE:
            await update.message.edit_caption(
                caption=Translation.RCHD_TG_API_LIMIT,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            start_time = time.time()
            if (await db.get_upload_as_doc(update.from_user.id)) is False:
                thumbnail = await Gthumb01(bot, update)
                await update.message.reply_document(
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
            else:
                width, height, duration = await Mdata01(download_directory)
                thumb_image_path = await Gthumb02(bot, update, duration, download_directory)
                await update.message.reply_video(
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    parse_mode=enums.ParseMode.HTML,
                    thumb=thumb_image_path,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )

            # Handling Audio and VM types
            if tg_send_type == "audio":
                duration = await Mdata03(download_directory)
                thumbnail = await Gthumb01(bot, update)
                await update.message.reply_audio(
                    audio=download_directory,
                    caption=description,
                    duration=duration,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
            elif tg_send_type == "vm":
                width, duration = await Mdata02(download_directory)
                thumbnail = await Gthumb02(bot, update, duration, download_directory)
                await update.message.reply_video_note(
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )

            end_two = datetime.now()
            # Cleanup Task ID
            if task_id in Config.DOWNLOAD_LOCATION:
                Config.DOWNLOAD_LOCATION.remove(task_id)

            try:
                os.remove(download_directory)
                if os.path.exists(thumb_image_path):
                    os.remove(thumb_image_path)
            except:
                pass

            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await update.message.edit_caption(
                caption=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await update.message.edit_caption(
            caption=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
            parse_mode=enums.ParseMode.HTML
        )

async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start, task_id):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers.get("Content-Length", 0))
        content_type = response.headers.get("Content-Type", "")
        
        if "text" in content_type and total_length < 500:
            return await response.release()

        with open(file_name, "wb") as f_handle:
            while True:
                # --- CRITICAL CANCEL CHECK ---
                if task_id not in Config.DOWNLOAD_LOCATION:
                    logger.info("Download cancelled by user.")
                    return False

                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += len(chunk)
                
                now = time.time()
                diff = now - start
                if round(diff % 4.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    eta = round((total_length - downloaded) / speed) * 1000 if speed > 0 else 0
                    
                    # Animated Progress Bar
                    progress_bar = "".join(["▰" for i in range(math.floor(percentage / 5))])
                    remaining_bar = "".join(["▱" for i in range(20 - math.floor(percentage / 5))])
                    
                    current_message = (
                        f"📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ Fɪʟᴇ...**\n"
                        f"┏━━━━━━━━━━━━━━━━━━━┓\n"
                        f"┣ [{progress_bar}{remaining_bar}]\n"
                        f"┣📦 **Pʀᴏɢʀᴇss :** {round(percentage, 2)}%\n"
                        f"┣✅ **Dᴏɴᴇ :** {humanbytes(downloaded)}\n"
                        f"┣📁 **Tᴏᴛᴀʟ :** {humanbytes(total_length)}\n"
                        f"┣⚡ **Sᴘᴇᴇᴅ :** {humanbytes(speed)}/s\n"
                        f"┣🕒 **ETA :** {TimeFormatter(eta)}\n"
                        f"┗━━━━━━━━━━━━━━━━━━━┛"
                    )

                    if current_message != display_message:
                        try:
                            await bot.edit_message_text(chat_id, message_id, text=current_message)
                            display_message = current_message
                        except:
                            pass
        return True
