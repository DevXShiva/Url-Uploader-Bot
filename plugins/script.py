from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation(object):

    START_TEXT = """✨ **Hᴇʟʟᴏ {} !**

I am a powerful **URL Uᴘʟᴏᴀᴅᴇʀ Bᴏᴛ** 🚀
I can upload any direct link to Telegram as a **File** or **Video** with high speed.

**Mᴀɪɴ Fᴇᴀᴛᴜʀᴇs:**
⚡️ Fast Download & Upload
🖼️ Custom Thumbnail Support
📝 Custom Caption Support
🎬 Video/File Selection Mode

Usᴇ **Hᴇʟᴘ** ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ!
"""

    HELP_TEXT = """📖 **Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ**

1️⃣ **Settings:** Use /settings to change upload mode (File/Video).
2️⃣ **Thumbnail:** Send any photo to set it as a permanent thumbnail.
3️⃣ **Uploading:** Send a Direct Link.
   *Example:* `https://link.com/file.mp4 | NewName.mp4`
4️⃣ **Caption:** Reply to any media with /caption to set custom text.

**Need Help? Join @devXvoid**
"""

    ABOUT_TEXT = """
╭───────────⍟
├🤖 **Mʏ Nᴀᴍᴇ** : URL Uᴘʟᴏᴀᴅᴇʀ Pʀᴏ
├🐍 **Lᴀɴɢᴜᴀɢᴇ** : Python 3.10+
├📦 **Fʀᴀᴍᴇᴡᴏʀᴋ** : Pyrogram 2.0.106
├📊 **Dᴀᴛᴀʙᴀsᴇ** : MongoDB (Fast)
├👤 **Dᴇᴠᴇʟᴏᴘᴇʀ** : @devXvoid
├📢 **Cʜᴀɴɴᴇʟ** : VoidXDev
├🛠️ **GɪᴛHᴜʙ** : [Sᴏᴜʀᴄᴇ Cᴏᴅᴇ](https://github.com/DevXShiva/Url-Uploader-Bot)
╰───────────────⍟
"""

    PROGRESS = """
🚀 **Uᴘʟᴏᴀᴅɪɴɢ Dᴇᴛᴀɪʟs**
┏━━━━━━━━━━━━━━━━━━━┓
┣📦 **Pʀᴏɢʀᴇss :** {0}%
┣✅ **Dᴏɴᴇ :** {1}
┣📁 **Tᴏᴛᴀʟ :** {2}
┣⚡ **Sᴘᴇᴇᴅ :** {3}/s
┣🕒 **ETA :** {4}
┗━━━━━━━━━━━━━━━━━━━┛
"""

    PROGRES = """`{}`\n{}"""

    INFO_TEXT = """
👤 **USER INFORMATION**
╭──────────────〄
├📛 **Fɪʀsᴛ Nᴀᴍᴇ :** <b>{}</b>
├📛 **Lᴀsᴛ Nᴀᴍᴇ :** <b>{}</b>
├👤 **Usᴇʀɴᴀᴍᴇ :** <b>@{}</b>
├🆔 **Tᴇʟᴇɢʀᴀᴍ ID :** <code>{}</code>
├🖇️ **Pʀᴏꜰɪʟᴇ Lɪɴᴋ :** <b>{}</b>
├📡 **Dᴄ :** <b>{}</b>
├💫 **Sᴛᴀᴛᴜs :** <b>{}</b>
╰──────────────────〄
"""

    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙️ SETTINGS', callback_data='OpenSettings')
        ],[
        InlineKeyboardButton('📖 HELP', callback_data='help'),
        InlineKeyboardButton('🎯 ABOUT', callback_data='about')
        ],[
        InlineKeyboardButton('📢 CHANNEL', url='https://t.me/devXvoid'),
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙️ SETTINGS', callback_data='OpenSettings')
        ],[
        InlineKeyboardButton('🔙 BACK', callback_data='home'),
        InlineKeyboardButton('🎯 ABOUT', callback_data='about')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📦 SOURCE CODE', url='https://github.com/DevXShiva/Url-Uploader-Bot')
        ],[
        InlineKeyboardButton('🔙 BACK', callback_data='home'),
        InlineKeyboardButton('📖 HELP', callback_data='help')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    
    PLANS_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎯 ABOUT', callback_data='about')
        ],[
        InlineKeyboardButton('🔙 BACK', callback_data='home'),
        InlineKeyboardButton('📖 HELP', callback_data='help')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    
    BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )

    INCORRECT_REQUEST = "❌ **Invalid Request!**"
    DOWNLOAD_FAILED = "❌ **Download Failed!**"
    TEXT = "Sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ"
    IFLONG_FILE_NAME = "⚠️ Only 64 characters allowed in filename."
    RENAME_403_ERR = "Sorry. You are not permitted to rename this file."
    ABS_TEXT = " Please don't be selfish."
    FORMAT_SELECTION = "<b>Sᴇʟᴇᴄᴛ Yᴏᴜʀ Fᴏʀᴍᴀᴛ 👇</b>\n"
    SET_CUSTOM_USERNAME_PASSWORD = """<b>🎥 Vɪᴅᴇᴏ = Uᴘʟᴏᴀᴅ As Sᴛʀᴇᴀᴍʙʟᴇ</b>\n\n<b>📂 Fɪʟᴇ = Uᴘʟᴏᴀᴅ As Fɪʟᴇ</b>\n\n<b>👮‍♂ Pᴏᴡᴇʀᴇᴅ Bʏ :</b> @devXvoid"""
    DOWNLOAD_START = "📥 **Downloading...**\n\n📂 **File:** `{}`"
    UPLOAD_START = "📤 **Uploading...**"
    RCHD_BOT_API_LIMIT = "Size greater than 50MB. Attempting upload..."
    RCHD_TG_API_LIMIT = "⚠️ File size is too large (2GB+). Telegram limits prevent upload."
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "✅ **Uploaded Successfully!**\n\nThank you for using @devXvoid bots!"
    SAVED_CUSTOM_THUMB_NAIL = "✅ **Thumbnail Saved!**"
    DEL_ETED_CUSTOM_THUMB_NAIL = "🗑️ **Thumbnail Deleted!**"
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared successfully."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_CUSTOM_THUMB_NAIL_FOUND = "❌ No custom thumbnail found."
    NO_VOID_FORMAT_FOUND = "❌ Error... <code>{}</code>"
    FILE_NOT_FOUND = "❌ Error: File not found!"
    FF_MPEG_RO_BOT_AD_VER_TISE_MENT = "Join @devXvoid for more awesome bots!"
    ADD_CAPTION_HELP = """**Hᴏᴡ Tᴏ Sᴇᴛ Cᴀᴘᴛɪᴏɴ?**\n\nForward me any Telegram file and reply with the text you want as caption. ✨"""
