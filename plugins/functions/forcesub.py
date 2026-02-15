import os
import asyncio
from plugins.config import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant, ChatAdminRequired, PeerIdInvalid, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def handle_force_subscribe(bot, message):
    # 1. Check if Channel is configured
    if not Config.UPDATES_CHANNEL:
        return 200 # Skip FSub if no channel ID

    try:
        # 2. Generate Invite Link (Requires Admin Rights)
        try:
            invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
            invite_url = invite_link.invite_link
        except Exception:
            # Fallback URL if bot is not admin or link creation fails
            invite_url = f"https://t.me/c/{str(Config.UPDATES_CHANNEL).replace('-100', '')}"

        # 3. Check User Membership
        user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), message.from_user.id)
        
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.from_user.id,
                text="❌ **Sᴏʀʀʏ, ʏᴏᴜ ᴀʀᴇ BANNED ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ.**",
                disable_web_page_preview=True,
            )
            return 400
        
        return 200 # User is a member, continue to bot commands

    except UserNotParticipant:
        # 4. User not in channel, show join button
        await bot.send_message(
            chat_id=message.from_user.id,
            text="**Pʟᴇᴀsᴇ Jᴏɪɴ Oᴜʀ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Tʜɪs Bᴏᴛ!**\n\nDᴜᴇ ᴛᴏ sᴇʀᴠᴇʀ ʟᴏᴀᴅ, ᴏɴʟʏ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ. Jᴏɪɴ ᴀɴᴅ ᴘʀᴇss ʀᴇғʀᴇsʜ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Join Channel 📢", url=invite_url)],
                    [InlineKeyboardButton("🔄 Refresh / Try Again", callback_data="refreshForceSub")]
                ]
            ),
        )
        return 400

    except (ChatAdminRequired, ChannelInvalid, PeerIdInvalid):
        # 5. Bot side error (Admin missing etc.) 
        # We return 200 so the user isn't stuck if the admin made a mistake
        print(f"DEBUG: ForceSub Error - Check if Bot is Admin in {Config.UPDATES_CHANNEL}")
        return 200

    except Exception as e:
        print(f"DEBUG: Unexpected ForceSub Error: {e}")
        return 200
