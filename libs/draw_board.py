import chess
import chess.svg
from cairosvg import svg2png

async def draw_board(message, board, caption=''):
    svg = chess.svg.board(board, size=350)
    svg2png(bytestring=svg, write_to='/tmp/output.png')

    with open('/tmp/output.png', 'rb') as photo:
        await message.answer_photo(photo=photo, caption=caption)

async def send_board(bot, user_id, board, caption=''):
    svg = chess.svg.board(board, size=350)
    svg2png(bytestring=svg, write_to='/tmp/output.png')

    with open('/tmp/output.png', 'rb') as photo:
        await bot.send_photo(chat_id=user_id, photo=photo, caption=caption)
