import os
import time
import psutil
import shutil
import string
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors import MessageNotModified

# Internal Imports
from plugins.config import Config
from plugins.script import Translation
from plugins.database.add import AddUser
from plugins.database.database import db
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.verify import verify_user, check_token

@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    # Force Subscribe Logic
    if Config.UPDATES_CHANNEL is not None:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return

    # Deep Link / Verify Logic
    if len(update.command) != 2:
        await AddUser(bot, update)
        await update.reply_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
        )
        return

    data = update.command[1]
    if data.startswith("verify"):
        try:
            _, userid, token = data.split("-", 2)
        except ValueError:
            return await update.reply_text("<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>")

        if str(update.from_user.id) != str(userid):
            return await update.reply_text("<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>")

        is_valid = await check_token(bot, userid, token)
        if is_valid:
            await update.reply_text(
                text=f"<b>Hᴇʏ {update.from_user.mention} 👋,\nʏᴏᴜ Aʀᴇ Sᴜᴄᴄᴇssғᴜʟʟʏ Vᴇʀɪғɪᴇᴅ !\n\nNᴏᴡ Yᴏᴜ Cᴀɴ Uᴘʟᴏᴀᴅ Fɪʟᴇs Aɴᴅ Vɪᴅᴇᴏs Uɴᴛɪʟ Mɪᴅɴɪɢʜᴛ.</b>"
            )
            await verify_user(bot, userid, token)
        else:
            await update.reply_text("<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>")

@Client.on_message(filters.command("help") & filters.private)
async def help_bot(_, m: Message):
    await AddUser(_, m)
    return await m.reply_text(
        text=Translation.HELP_TEXT,
        reply_markup=Translation.HELP_BUTTONS,
        disable_web_page_preview=True,
    )

@Client.on_message(filters.command("about") & filters.private)
async def aboutme(_, m: Message):
    await AddUser(_, m)
    return await m.reply_text(
        text=Translation.ABOUT_TEXT,
        reply_markup=Translation.ABOUT_BUTTONS,
        disable_web_page_preview=True,
    )

@Client.on_message(filters.private & filters.reply & filters.text)
async def edit_caption(bot, update):
    """Replies to a video/document with text to change caption."""
    await AddUser(bot, update)
    replied_msg = update.reply_to_message
    if replied_msg.video or replied_msg.document:
        file_id = replied_msg.video.file_id if replied_msg.video else replied_msg.document.file_id
        try:
            await bot.send_cached_media(
                chat_id=update.chat.id,
                file_id=file_id,
                caption=update.text
            )
        except Exception as e:
            print(f"Caption Error: {e}")

@Client.on_message(filters.private & filters.command("caption"))
async def add_caption_help(bot, update):
    await AddUser(bot, update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ADD_CAPTION_HELP,
        reply_markup=Translation.BUTTONS,
    )

@Client.on_callback_query(filters.regex('^cancel_download\+'))
async def cancel_cb(c, m: CallbackQuery):
    """Professional Cancel Logic to prevent Bot Jamming."""
    task_id = m.data.split("+", 1)[1]
    
    # Check if task exists in the list
    if task_id not in Config.DOWNLOAD_LOCATION:
        await m.answer("Process already finished or cancelled! ⚠️", show_alert=True)
        await m.message.edit_text("❌ **No Active Task Found.**")
        return

    # Remove from list (This signals the progress bar to stop)
    Config.DOWNLOAD_LOCATION.remove(task_id)
    
    await m.answer("Cancelling... 🛑", show_alert=True)
    await m.message.edit_text("🔄 **Cancelling Process...**\nCleaning up resources.")
    
    # Wait a moment for the background process to detect the removal
    await asyncio.sleep(2)
    await m.message.edit_text("✅ **Successfully Cancelled.**\nYou can send a new link now.")

@Client.on_message(filters.private & filters.command("info"))
async def info_handler(bot, update):
    user = update.from_user
    last_name = user.last_name if user.last_name else "None"
    await update.reply_text(  
        text=Translation.INFO_TEXT.format(
            user.first_name, last_name, user.username, user.id, 
            user.mention, user.dc_id, user.language_code, user.status
        ), 
        reply_markup=Translation.BUTTONS,           
        disable_web_page_preview=True
    )

@Client.on_message(filters.private & filters.command("warn"))
async def warn(c, m):
    # Check if user is in sudo/admin list
    if m.from_user.id in Config.ADMIN:
        if len(m.command) >= 3:
            try:
                user_id = int(m.text.split(' ', 2)[1])
                reason = m.text.split(' ', 2)[2]
                await c.send_message(chat_id=user_id, text=f"⚠️ **WARNING:**\n\n{reason}")
                await m.reply_text(f"✅ User `{user_id}` notified successfully.")
            except Exception as e:
                await m.reply_text(f"❌ **Error:**\n`{e}`")
        else:
            await m.reply_text("📊 **Usage:** `/warn user_id reason`")
    else:
        await m.reply_text("😡 **You are not authorized to use this command!**")
