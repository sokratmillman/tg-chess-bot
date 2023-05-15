from aiogram import Bot
from aiogram.types import BotCommand

from texts import (
    CANCEL_GAME_COMMAND, GET_MY_ID_COMMAND,
    HELP_COMMAND, START_AI_GAME_COMMAND,
    START_COMMAND, START_PVP_GAME_COMMAND,
    LEADERBOARD_COMMAND, MY_HISTORY_COMMAND,
    MY_STATS_COMMAND, MATCH_STATS_COMMAND
)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description=START_COMMAND),
        BotCommand(command="/help", description=HELP_COMMAND),
        BotCommand(command="/get_my_id", description=GET_MY_ID_COMMAND),
        BotCommand(command="/start_ai_game", description=START_AI_GAME_COMMAND),
        BotCommand(command="/start_pvp_game", description=START_PVP_GAME_COMMAND),
        BotCommand(command="/cancel_game", description=CANCEL_GAME_COMMAND),
        BotCommand(command="/my_stats", description=MY_STATS_COMMAND),
        BotCommand(command="/my_history", description=MY_HISTORY_COMMAND),
        BotCommand(command="/leaderboard", description=LEADERBOARD_COMMAND),
        BotCommand(command="/match_stats", description=MATCH_STATS_COMMAND)
    ]
    await bot.set_my_commands(commands)
