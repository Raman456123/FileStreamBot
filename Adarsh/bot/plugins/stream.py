#(c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


MY_PASS = os.environ.get("MY_PASS",None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("loginπ") | filters.command("login")) & ~filters.edited, group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("π½ππ  ππππ ππππ πΏππππ πππ.\n\n Ιͺκ° Κα΄α΄ α΄α΄Ι΄'α΄ α΄Ι΄α΄α΄‘ α΄Κα΄α΄α΄ α΄Κα΄ MY_PASS α΄ α΄ΚΙͺα΄ΚΚα΄ ΙͺΙ΄ Κα΄Κα΄α΄α΄ \n\n(Κα΄α΄ α΄α΄Ι΄ α΄κ±α΄/cancel α΄α΄α΄α΄α΄Ι΄α΄ α΄α΄ α΄α΄Ι΄α΄α΄Κ α΄Κα΄ α΄Κα΄α΄α΄κ±κ±)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp=="/cancel":
                   await ag.edit("Process Cancelled Successfully")
                   return
            else:
                return
        except TimeoutError:
            await ag.edit("I can't Wait More For Password, Try Again")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "Yeah! You Entered The Password Correctly"
        else:
            ag_text = "Wrong Password, Try Again"
        await ag.edit(ag_text)
    except Exception as e:
        print(e)

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) & ~filters.edited, group=4)
async def private_receive_handler(c: Client, m: Message):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass== None:
            await m.reply_text("Login First Using /login CMD \n don\'t Know The Pass? Request It From @ChVivekTomar")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"Nα΄α΄‘ Usα΄Κ Jα΄ΙͺΙ΄α΄α΄ : \n\n Nα΄α΄α΄ : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sα΄α΄Κα΄α΄α΄ Yα΄α΄Κ Bα΄α΄ !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="__Sα΄ΚΚΚ SΙͺΚ, Yα΄α΄ α΄Κα΄ Bα΄Ι΄Ι΄α΄α΄ α΄α΄ α΄sα΄ α΄α΄.__\n\n  **Cα΄Ι΄α΄α΄α΄α΄ Dα΄α΄ α΄Κα΄α΄α΄Κ @Pravin_boopathi Κα΄ WΙͺΚΚ Hα΄Κα΄ Yα΄α΄**",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>α΄α΄ΙͺΙ΄ α΄α΄α΄α΄α΄α΄κ± α΄Κα΄Ι΄Ι΄α΄Κκ± α΄α΄ α΄κ±α΄ α΄α΄ π</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jα΄ΙͺΙ΄ Ι΄α΄α΄‘ π", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="HTML"
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**Sα΄α΄α΄α΄ΚΙͺΙ΄Ι’ α΄‘α΄Ι΄α΄ WΚα΄Ι΄Ι’. Cα΄Ι΄α΄α΄α΄α΄ α΄Κ Κα΄ss** @Pravin_boopathi",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    try:

        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        
        online_link = f"{Var.URL}{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
       
        
        

        msg_text ="""
<i><u>ππ¨π?π« ππ’π§π€ ποΈ πππ§ππ«ππ­ππ ππ?ππππ¬π¬ππ?π₯π₯π²!</u></i>

<b>π ππ’π₯π πππ¦π :</b> <i>{}</i>

<b>β³ ππ’π₯π ππ’π³π :</b> <i>{}</i>

<b>π₯ ππ¨π°π§π₯π¨ππ ππ’π§π€ :</b> <code>https://droplink.kalvidudes.in/st?api=091f2c0a78b3766954c7dae3dffed779d8740a30&url={}</code>

<b>ποΈ ππ§π₯π’π§π ππ­π«πππ¦ ππ’π§π€ :</b> <code>https://droplink.kalvidudes.in/st?api=091f2c0a78b3766954c7dae3dffed779d8740a30&url={}</code>

<b>π ππ¨π­π 1 : ππ’π§π€ ππ¨π§'π­ ππ±π©π’π«π ππ§π­π’π₯π₯ π πππ₯ππ­π.</b>

<b>π ππ¨π­π 2 : ππ ππ’π₯π₯ ππππ¨π¦π¦ππ§π ππ¨π? ππ¨ ππ¬π πππ , πππ ππ πππ ππ¨ ππ¨π°π§π₯π¨ππ ππ’π₯π ππ?π’ππ€π₯π².</b>"""

        await log_msg.reply_text(text=f"**Rα΄Qα΄α΄κ±α΄α΄α΄ ΚΚ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uκ±α΄Κ Ιͺα΄ :** `{m.from_user.id}`\n**Stream ΚΙͺΙ΄α΄ :** {stream_link}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            parse_mode="HTML", 
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("π₯α΄Ι΄ΚΙͺΙ΄α΄ κ±α΄Κα΄α΄α΄ ποΈ", url=stream_link), #Stream Link
                                                InlineKeyboardButton('Dα΄α΄‘Ι΄Κα΄α΄α΄ π₯', url=online_link)]]) #Download Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gα΄α΄ FΚα΄α΄α΄Wα΄Ιͺα΄ α΄? {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**ππππ πΈπ³ :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.edited & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("Login First Using /login CMD \n don\'t Know The Pass? Request It From @ChVivekTomar")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong Password, Login Again")
            await pass_db.delete_user(broadcast.chat.id)
            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{quote_plus(get_name(log_msg))}/{str(log_msg.message_id)}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{quote_plus(get_name(log_msg))}/{str(log_msg.message_id)}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**CΚα΄Ι΄Ι΄α΄Κ Nα΄α΄α΄:** `{broadcast.chat.title}`\n**CΚα΄Ι΄Ι΄α΄Κ ID:** `{broadcast.chat.id}`\n**Rα΄Η«α΄α΄sα΄ α΄ΚΚ:** {stream_link}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("π₯α΄Ι΄ΚΙͺΙ΄α΄ κ±α΄Κα΄α΄α΄ ποΈ", url=stream_link),
                     InlineKeyboardButton('Dα΄α΄‘Ι΄Κα΄α΄α΄ π₯', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gα΄α΄ FΚα΄α΄α΄Wα΄Ιͺα΄ α΄? {str(w.x)}s from {broadcast.chat.title}\n\n**CΚα΄Ι΄Ι΄α΄Κ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#α΄ΚΚα΄Κ_α΄Κα΄α΄α΄Κα΄α΄α΄:** `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
        print(f"Cα΄Ι΄'α΄ Eα΄Ιͺα΄ BΚα΄α΄α΄α΄α΄sα΄ Mα΄ssα΄Ι’α΄!\nEΚΚα΄Κ:  **Give me edit permission in updates and bin Chanell{e}**")
