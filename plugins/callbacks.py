import os
import asyncio
import logging
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from plugins.functions.display_progress import progress_for_pyrogram, humanbytes
from plugins.config import Config
from plugins.dl_button import ddl_call_back
from plugins.button import youtube_dl_call_back
from plugins.settings.settings import OpenSettings
from plugins.script import Translation
from plugins.database.database import db

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@Client.on_callback_query()
async def button(bot, update: CallbackQuery):
    if update.data == "home":
        await update.message.edit(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
        )
    elif update.data == "help":
        await update.message.edit(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
        )
    elif update.data == "about":
        await update.message.edit(
            text=Translation.ABOUT_TEXT,
            reply_markup=Translation.ABOUT_BUTTONS,
        )
    
    # --- Force Subscribe Refresh Logic ---
    elif "refreshForceSub" in update.data:
        if Config.UPDATES_CHANNEL:
            channel_id = int(Config.UPDATES_CHANNEL)
            try:
                user = await bot.get_chat_member(channel_id, update.from_user.id)
                if user.status == "kicked":
                    await update.answer("You are banned! ❌", show_alert=True)
                    return
            except Exception:
                # User joined nahi hai ya bot admin nahi hai
                await update.answer("Please join the channel first! 😑", show_alert=True)
                return
            
            # Agar join kar liya hai toh start text bhejein
            await update.message.edit(
                text=Translation.START_TEXT.format(update.from_user.mention),
                reply_markup=Translation.START_BUTTONS,
            )
        else:
            await update.answer("Force Subscribe not configured!")

    # --- Cancel Download Logic ---
    elif update.data.startswith("cancel_download+"):
        task_id = update.data.split("+", 1)[1]
        if isinstance(Config.DOWNLOAD_LOCATION, list) and task_id in Config.DOWNLOAD_LOCATION:
            Config.DOWNLOAD_LOCATION.remove(task_id)
            await update.answer("Cancelling... 🛑", show_alert=True)
            await update.message.edit_text("🔄 **Cancelling Process...**\nCleaning up resources.")
        else:
            await update.answer("Task already finished or not found! ⚠️", show_alert=True)

    elif update.data == "OpenSettings":
        await update.answer()
        await OpenSettings(update.message)
    
    elif update.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(update.from_user.id)
        if not thumbnail:
            await update.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await update.answer()
            await bot.send_photo(update.message.chat.id, thumbnail, "Custom Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Delete Thumbnail",
                                                              callback_data="deleteThumbnail")
                               ]]))
    
    elif update.data == "deleteThumbnail":
        await db.set_thumbnail(update.from_user.id, None)
        await update.answer("Okay, I deleted your custom thumbnail.", show_alert=True)
        await update.message.delete(True)

    elif update.data == "setThumbnail":
        await update.message.edit(
            text=Translation.TEXT,
            reply_markup=Translation.BUTTONS,
            disable_web_page_preview=True
        )

    elif update.data == "triggerGenSS":
        await update.answer()
        generate_ss = await db.get_generate_ss(update.from_user.id)
        await db.set_generate_ss(update.from_user.id, not generate_ss)
        await OpenSettings(update.message)

    elif update.data == "triggerGenSample":
        await update.answer()
        gen_sample = await db.get_generate_sample_video(update.from_user.id)
        await db.set_generate_sample_video(update.from_user.id, not gen_sample)
        await OpenSettings(update.message)

    elif update.data == "triggerUploadMode":
        await update.answer()
        upload_doc = await db.get_upload_as_doc(update.from_user.id)
        await db.set_upload_as_doc(update.from_user.id, not upload_doc)
        await OpenSettings(update.message)

    elif "close" in update.data:
        await update.message.delete(True)

    elif "|" in update.data:
        await youtube_dl_call_back(bot, update)
        
    elif "=" in update.data:
        await ddl_call_back(bot, update)

    else:
        await update.message.delete()
