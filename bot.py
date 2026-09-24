import os
import asyncio
from aiohttp import web
from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot चालू है!\n\n"
        "/lock - Group lock\n"
        "/unlock - Group unlock\n"
        "/warn - Warning message\n"
        "/id - Group ID"
    )


async def is_admin(update: Update):
    member = await update.effective_chat.get_member(
        update.effective_user.id
    )
    return member.status in ("administrator", "creator")


async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    permissions = ChatPermissions(
        can_send_messages=False
    )

    await update.effective_chat.set_permissions(
        permissions=permissions
    )

    await update.message.reply_text(
        "🔒 GROUP LOCKED\n\n"
        "⚠️ अभी केवल Admin message भेज सकते हैं।"
    )


async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    await update.effective_chat.set_permissions(
        permissions=permissions
    )

    await update.message.reply_text(
        "🔓 GROUP UNLOCKED\n\n"
        "✅ अब members message भेज सकते हैं।"
    )


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    await update.message.reply_text(
        "⚠️⚠️ आवश्यक सूचना ⚠️⚠️\n\n"
        "🚨 सभी सदस्य ध्यान दें 🚨\n\n"
        "❌ किसी भी व्यक्ति को अपना OTP न दें।\n"
        "❌ किसी अनजान व्यक्ति को personal payment न करें।\n\n"
        "🙏 सावधान रहें और सुरक्षित रहें।"
    )


async def group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 Group ID:\n`{update.effective_chat.id}`",
        parse_mode="Markdown"
    )


async def health(request):
    return web.Response(text="Bot is running ✅")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable missing")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lock", lock))
    application.add_handler(CommandHandler("unlock", unlock))
    application.add_handler(CommandHandler("warn", warn))
    application.add_handler(CommandHandler("id", group_id))

    await start_web_server()

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("Bot started successfully ✅")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main()) 
