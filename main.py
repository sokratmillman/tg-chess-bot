import asyncio

from handlers.ai_game_handlers import register_ai_game_handlers
from handlers.common_handlers import register_common_handlers
from handlers.pvp_game_handlers import register_pvp_game_handlers
from handlers.set_commands import set_commands

from bot import bot, dp


async def main():
    register_common_handlers(dp)
    register_ai_game_handlers(dp)
    register_pvp_game_handlers(dp)
    await set_commands(bot)
    await dp.skip_updates()
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
