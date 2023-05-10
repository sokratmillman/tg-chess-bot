from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import chess
import chess.svg

from const import AVAILABLE
from firebase.db_handlers import database, handle_game_reject, handle_game_request, handle_game_start, handle_game_finish
from handlers.state import ChessState
from keyboards.accept_invite import accept_invite_kb, AGREE_TEXT, DISAGREE_TEXT
from libs.draw_board import draw_board, send_board
from bot import bot, dp
from texts import CANCEL_INVITE_TEXT, DRAW_TEXT, INVALID_MOVE_TEXT, INVITE_REJECTED_TEXT, NOT_YOUR_TURN_TEXT, GAME_STARTED_TEXT, USER_MOVE_TEXT, WAIT_OPPONENT_MOVE_TEXT, WAITING_INVITE_TEXT, WIN_TEXT, WRONG_ID_TEXT

async def start_pvp_game(message: types.Message, state: FSMContext):
    try:
        partner_id = message.get_args().split()[0]
    except Exception:
        await message.answer('Please, provide partner id. Example: `/start_pvp_game 1235`', parse_mode="Markdown")
        return
    
    try:
        partner_state = dp.current_state(user=partner_id, chat=partner_id)

        await message.answer(WAITING_INVITE_TEXT.format(partner_id), parse_mode="Markdown")
        await bot.send_message(partner_id, f'Let\'s play with {message.from_user.username}!', reply_markup=accept_invite_kb)
        await state.set_state(ChessState.WAITING.state)
        await partner_state.set_state(ChessState.WAITING.state)

        handle_game_request(message.from_user.id, partner_id)
    except Exception:
        await message.answer(WRONG_ID_TEXT)

async def waiting_handler(message: types.Message, state: FSMContext):
    if (message.text == AGREE_TEXT):
        board = chess.Board()

        me = database.get_user(message.from_user.id)
        partner_id = me['status'].split(' ')[-1]

        handle_game_start(partner_id, str(message.from_user.id))

        await draw_board(message, board, WAIT_OPPONENT_MOVE_TEXT)
        await send_board(bot, partner_id, board, GAME_STARTED_TEXT)
    elif (message.text == DISAGREE_TEXT):
        me = database.get_user(message.from_user.id)
        partner_id = me['status'].split(' ')[-1]

        handle_game_reject(message.from_user.id, partner_id)

        await message.answer(CANCEL_INVITE_TEXT)
        await bot.send_message(partner_id, INVITE_REJECTED_TEXT.format(message.from_user.username))
        
        partner_state = dp.current_state(user=partner_id, chat=partner_id)
        await partner_state.finish()
        await state.finish()

async def game_handler(message: types.Message, state: FSMContext):
    user = database.get_user(message.from_user.id)
    game_id = user['current_game']
    if (game_id == '-1'):
        # no game in progress, ignore
        return
    game = database.get_game(game_id)
    white_id = game['white']
    black_id = game['black']
    if (game['current_turn'] != str(message.from_user.id)):
        # not my turn
        await message.answer(NOT_YOUR_TURN_TEXT)
        return
    
    partner_id = white_id if str(message.from_user.id) != white_id else black_id
    
    board = chess.Board(game['board'])
    board.turn = chess.WHITE if str(message.from_user.id) == white_id else chess.BLACK

    try:
        board.push_san(message.text)

        database.update_game(game_id, {"current_turn": str(partner_id), "board": board.fen()})

        end_text = ''
        if (board.is_game_over()):

            if (board.is_stalemate()):
                end_text = DRAW_TEXT
                handle_game_finish(game_id, 'draw' , 'pvp')
            else:
                game = database.get_game(game_id)
                white_id = game['white']
                black_id = game['black']
                amiwhite = str(message.from_user.id) == white_id
                handle_game_finish(game_id, 'win', 'pvp', 'white' if amiwhite else 'black')

            end_text = WIN_TEXT.format(message.from_user.username)

            partner_state = dp.current_state(user=partner_id, chat=partner_id)
            await partner_state.finish()
            await state.finish()

        await send_board(bot, partner_id, board, USER_MOVE_TEXT.format(message.from_user.username, message.text) if end_text == '' else end_text)
        await draw_board(message, board, WAIT_OPPONENT_MOVE_TEXT if end_text == '' else end_text)
    except Exception:
        await message.answer(INVALID_MOVE_TEXT)


def register_pvp_game_handlers(dp: Dispatcher):
    dp.register_message_handler(start_pvp_game, commands="start_pvp_game")
    dp.register_message_handler(waiting_handler, state=ChessState.WAITING)
    dp.register_message_handler(game_handler, state=ChessState.PVP_GAME)
