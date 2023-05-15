from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


from firebase.db_handlers import (
    database, handle_game_finish,
    handle_getting_playing, handle_getting_pending,
)

from bot import bot, dp
from handlers.state import ChessState
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
    if game_id == '-1':
        await message.answer(NO_GAME_YET_TEXT)
        await state.finish()
        return

    game = database.get_game(game_id)
    white_id = game['white']
    black_id = game['black']
    if black_id == '0':
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

    result = f"Top-{len(leaders)} players:\n\n"
    for key in leaders:
        result += f"{key}. {leaders[key]}\n"
    await message.answer(result)


async def my_history(message: types.Message):
    history = database.get_user_history(message.from_user.id)

    if history == '':
        await message.answer("No recent games")
        return

    history_list = history.split(", ")[:-1]
    result = "Recent games:\n\n"
    for rec_game in history_list:
        state, u_id = rec_game.split(" ")[0], rec_game.split(" ")[1]
        if state == "win":
            result += f"You won {u_id}\n"
        elif state == "loss":
            result += f"You lost to {u_id}\n"
        else:
            result += f"Draw with {u_id}\n"
    await message.answer(result)


async def my_stats(message: types.Message):
    stats = database.get_user_stats(message.from_user.id)

    result = "Your statistics:\n\n"
    result += f"Total games: {stats['total games']}\n"
    result += f"Wins: {stats['wins']}\n"
    result += f"Losses: {stats['losses']}\n"
    result += f"Draws: {stats['draws']}\n"
    result += f"% of wins: {stats['% of wins']}"

    await message.answer(result)


async def on_startup():
    playing_ids_pairs = handle_getting_playing()
    pending_ids = handle_getting_pending()

    if pending_ids is not None:
        for uid in pending_ids:
            state = dp.current_state(user=uid, chat=uid)
            await state.set_state(ChessState.WAITING.state)

    if playing_ids_pairs is not None:
        for pair in playing_ids_pairs:
            if pair[0]!="0" and pair[1]!="0":
                state = dp.current_state(user=pair[0], chat=pair[0])
                partner_state = dp.current_state(user=pair[1], chat=pair[1])
                await state.set_state(ChessState.PVP_GAME.state)
                await partner_state.set_state(ChessState.PVP_GAME.state)
            else:
                player_id = pair[0] if pair[0]!="0" else pair[1]
                state = dp.current_state(user=player_id, chat=player_id)
                await state.set_state(ChessState.AI_GAME.state)


def register_common_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands="start")
    dispatcher.register_message_handler(get_info, commands="help", state="*")
    dispatcher.register_message_handler(get_my_id, commands="get_my_id", state="*")
    dispatcher.register_message_handler(cancel_game, commands="cancel_game", state="*")
    dispatcher.register_message_handler(my_stats, commands="my_stats", state="*")
    dispatcher.register_message_handler(my_history, commands="my_history", state="*")
    dispatcher.register_message_handler(leaderboard, commands="leaderboard", state="*")
