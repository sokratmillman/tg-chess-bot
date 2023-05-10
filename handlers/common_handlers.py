from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from const import AVAILABLE

from firebase.db_handlers import database, handle_game_finish
from bot import bot, dp
from texts import GAME_CANCELLED_TEXT, HELP_TEXT, NO_GAME_YET_TEXT, YOUR_ID_TEXT

async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm ChessBot!\nPowered by aiogram.")

    database.create_user(message.from_user.id)

async def get_info(message: types.Message):
    await message.answer(HELP_TEXT, parse_mode='Markdown')

async def get_my_id(message: types.Message):
    
    await message.answer(YOUR_ID_TEXT.format(message.from_user.id), parse_mode='Markdown')

async def cancel_game(message: types.Message, state: FSMContext):
    user = database.get_user(message.from_user.id)
    if user is None:
        await state.finish()
        await message.answer(GAME_CANCELLED_TEXT)
        return
    
    game_id = user['current_game']
    if (game_id == '-1'):
        await message.answer(NO_GAME_YET_TEXT)
        await state.finish()
        return
    
    game = database.get_game(game_id)
    white_id = game['white']
    black_id = game['black']
    if (black_id == '0'):
        await message.answer(GAME_CANCELLED_TEXT)
        await state.finish()
        user = database.get_user(message.from_user.id)
        game_id = user['current_game']
        handle_game_finish(game_id, 'canceled', 'ai')
        return
    
    partner_id = white_id if str(message.from_user.id) != white_id else black_id
    partner_state = dp.current_state(user=partner_id, chat=partner_id)
    await partner_state.finish()
    await state.finish()
    
    await message.answer(GAME_CANCELLED_TEXT)
    await bot.send_message(partner_id, GAME_CANCELLED_TEXT)
    handle_game_finish(game_id, 'canceled', 'pvp')

async def leaderboard(message: types.Message):
    leaders = database.get_leaderboard()

    if leaders is None:
        await message.answer("No leaders yet")
        return

    result = f"Top-{len(leaders)} players:"
    for key in leaders:
        result += f"{key}. {leaders[key]}\n"
    await message.answer(result)

async def my_history(message: types.Message):
    history = database.get_user_history(message.from_user.id)

    if history == '':
        await message.answer("No recent games")
        return

    history_list = history.split(", ")[:-1]
    result = f"Recent games:\n\n"
    for el in history_list:
        state, id = el.split(" ")[0], el.split(" ")[1]
        if state == "won":
            result += f"You won {id}\n"
        elif state == "loss":
            result += f"You lost to {id}\n"
        else:
            result += f"Draw with {id}\n"
    await message.answer(result)

async def my_stats(message: types.Message):
    stats = database.get_user_stats(message.from_user.id)

    result = f"Your statistics:\n\n"
    result += f"Total games: {stats['total games']}\n"
    result += f"Wins: {stats['wins']}\n"
    result += f"Losses: {stats['losses']}\n"
    result += f"Draws: {stats['draws']}\n"
    result += f"% of wins: {stats['% of wins']}"
    
    await message.answer(result)

def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands="start")
    dp.register_message_handler(get_info, commands="help", state="*")
    dp.register_message_handler(get_my_id, commands="get_my_id", state="*")
    dp.register_message_handler(cancel_game, commands="cancel_game", state="*")
    dp.register_message_handler(my_stats, commands="my_stats", state="*")
    dp.register_message_handler(my_history, commands="my_history", state="*")
    dp.register_message_handler(leaderboard, commands="leaderboard", state="*")
