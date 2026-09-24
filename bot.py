import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Bot, ChatPermissions

BOT_TOKEN = os.environ["BOT_TOKEN"]

GROUP_1 = -1003983844612
GROUP_2 = -1004327618398

IST = ZoneInfo("Asia/Kolkata")


def get_open_group():
    now = datetime.now(IST)
    minutes = now.hour * 60 + now.minute

    # 1:00 PM - 2:50 PM
    if 13 * 60 <= minutes < 14 * 60 + 50:
        return GROUP_1

    # 3:00 PM - 4:30 PM
    if 15 * 60 <= minutes < 16 * 60 + 30:
        return GROUP_2

    # 5:00 PM - 5:50 PM
    if 17 * 60 <= minutes < 17 * 60 + 50:
        return GROUP_1

    # 6:00 PM - 9:50 PM
    if 18 * 60 <= minutes < 21 * 60 + 50:
        return GROUP_2

    # 10:00 PM - 3:00 AM
    if minutes >= 22 * 60 or minutes < 3 * 60:
        return GROUP_1

    # बाकी समय दोनों LOCK
    return None


async def set_lock(bot, chat_id, locked):
    permissions = ChatPermissions(
        can_send_messages=not locked,
        can_send_audios=not locked,
        can_send_documents=not locked,
        can_send_photos=not locked,
        can_send_videos=not locked,
        can_send_video_notes=not locked,
        can_send_voice_notes=not locked,
        can_send_polls=not locked,
        can_send_other_messages=not locked,
        can_add_web_page_previews=not locked,
    )

    await bot.set_chat_permissions(
        chat_id=chat_id,
        permissions=permissions
    )


async def main():
    bot = Bot(BOT_TOKEN)

    open_group = get_open_group()

    if open_group == GROUP_1:
        await set_lock(bot, GROUP_1, False)
        await set_lock(bot, GROUP_2, True)
        print("GROUP 1 OPEN - GROUP 2 LOCK")

    elif open_group == GROUP_2:
        await set_lock(bot, GROUP_1, True)
        await set_lock(bot, GROUP_2, False)
        print("GROUP 1 LOCK - GROUP 2 OPEN")

    else:
        await set_lock(bot, GROUP_1, True)
        await set_lock(bot, GROUP_2, True)
        print("BOTH GROUPS LOCK")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
