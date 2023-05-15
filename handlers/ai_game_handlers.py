from aiogram import  Dispatcher, types
from aiogram.dispatcher import FSMContext
import chess
import chess.svg
from stockfish import Stockfish

from handlers.state import ChessState

from libs.draw_board import draw_board

from firebase.db_handlers import database, handle_game_start, handle_game_finish

from texts import (
    AI_WON_TEXT, COMPUTER_MOVE, DRAW_TEXT, INVALID_MOVE_TEXT,
    NOT_YOUR_TURN_TEXT, GAME_STARTED_TEXT,
    WIN_TEXT, WRONG_START_TEXT,
)


stockfish = Stockfish(path="./Stockfish/src/stockfish")
stockfish.depth = 1

async def start_ai_game(message: types.Message, state: FSMContext):
    board = chess.Board()

    user = database.get_user(message.from_user.id)

    if user is None:
        await message.answer(WRONG_START_TEXT)
        await state.finish()
        return

    await draw_board(message, board)

    await message.answer(GAME_STARTED_TEXT)
    await state.set_state(ChessState.AI_GAME.state)

    handle_game_start(str(message.from_user.id), 0)

async def ai_make_turn(message: types.Message, state: FSMContext):
    user = database.get_user(message.from_user.id)
    if user is None:
        await state.finish()
        return
    game_id = user['current_game']
    if game_id == '-1':
        # no game in progress, ignore
        await state.finish()
        return
    game = database.get_game(game_id)

    if game['current_turn'] != str(message.from_user.id):
        await message.answer(NOT_YOUR_TURN_TEXT)
        return

    partner_id = 0

    board = chess.Board(game['board'])
    board.turn = chess.WHITE

    try:
        stockfish.set_fen_position(board.fen())
        possible_best_move = stockfish.get_best_move()
        board.push_san(message.text)
        best_move_msg = (f"Nice move, but I would go {possible_best_move}" 
                         if possible_best_move != message.text 
                         else "Exactly how I would move!")
        await message.answer(best_move_msg)
        await draw_board(message, board)
        database.update_game(game_id, {"current_turn": str(partner_id), "board": board.fen()})

        if board.is_game_over():
            if board.is_checkmate():
                handle_game_finish(game_id, 'win', 'ai', 'white')
                await message.answer(WIN_TEXT.format('You'))
            else:
                handle_game_finish(game_id, 'draw', 'ai', 'white')
                await message.answer(DRAW_TEXT)
            await state.finish()

        else:
            partner_id = message.from_user.id

            board = chess.Board(board.fen())
            board.turn = chess.BLACK

            stockfish.set_fen_position(board.fen())

            best_move = stockfish.get_best_move()
            board.push_san(best_move)

            await message.answer(COMPUTER_MOVE.format(best_move))
            await draw_board(message, board)

            if board.is_game_over():
                if board.is_checkmate():
                    handle_game_finish(game_id, 'win', 'ai')
                    await message.answer(AI_WON_TEXT)
                else:
                    await message.answer(DRAW_TEXT)
                await state.finish()

            database.update_game(game_id, {"current_turn": str(partner_id), "board": board.fen()})
    except Exception:
        await message.answer(INVALID_MOVE_TEXT)

async def match_stats(message: types.Message, state: FSMContext):
    user = database.get_user(message.from_user.id)
    if user is None:
        await state.finish()
        return
    game_id = user['current_game']
    
    curr_state = await state.get_state()

    if curr_state != ChessState.AI_GAME.state:
        await message.answer("No current game vs AI")
        return
    if game_id == '-1':
        # no game in progress, ignore
        await message.answer("No current game vs AI")
        await state.finish()
        return
    game = database.get_game(game_id)

    partner_id = 0

    board = chess.Board(game['board'])
    board.turn = chess.WHITE

    try:
        stockfish.set_fen_position(board.fen())
        eval = stockfish.get_evaluation()
        wdl = stockfish.get_wdl_stats()
        res = ""
        if eval['type'] == 'cp':
            res = f"Evaluation in centipawns: {eval['value']}\n\n"
        res += f"Current Win-Draw-Loss chances:\n"
        res += f"Win: {wdl[0]/1000}\n"
        res += f"Draw: {wdl[1]/1000}\n"
        res += f"Loss: {wdl[2]/1000}\n"
        await message.answer(res)
    except:
        pass

def register_ai_game_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_ai_game, commands="start_ai_game")
    dispatcher.register_message_handler(match_stats, commands="match_stats", state="*")
    dispatcher.register_message_handler(ai_make_turn, state=ChessState.AI_GAME)
