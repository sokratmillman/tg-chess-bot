AGREE_TEXT = 'Let\'s go! 👋'
DISAGREE_TEXT = 'Not now.. 👋'


START_COMMAND = 'Start Bot'
HELP_COMMAND = 'Rules of the Game'
GET_MY_ID_COMMAND = 'Get your game id'
START_AI_GAME_COMMAND = 'Start Game with AI'
START_PVP_GAME_COMMAND = 'Start Game with another person. Example /start_pvp_game 1235'
CANCEL_GAME_COMMAND = 'Cancel Game'
LEADERBOARD_COMMAND = 'Show table of the most winning players'
MY_HISTORY_COMMAND = 'Show most recent games'
MY_STATS_COMMAND = 'Show my statistics'



HELP_TEXT = """Welcome to ChessBot 👋

There are two modes:
\* Playing with a friend
\* Playing with a bot

Playing with a friend:
1. To play with a friend, your friend must press the `/start` command in the bot to register
2. A friend should get his ID by writing the command `/get_my_id`
3. A friend needs to send you his ID and you can invite him to the game with the command `/start_pvp_game [FRIEND_ID]`
4. A friend needs to agree and the game will start

Playing with a bot:
It is enough to run the command `/start_ai_game` and the game with the bot will begin

How to make moves:
To make a move, write in this form _[start position][final position]_
For example, to make the central pawn move forward in the starting position, you need to write to the chat _e2e4_"""

YOUR_ID_TEXT = 'Your id is `{}`'
NO_GAME_YET_TEXT = 'No game started yet'
GAME_CANCELLED_TEXT = 'Game canceled'
WRONG_START_TEXT = 'Something\'s wrong with your session. Send bot /start command again'
AI_WON_TEXT = 'Computer won'
WAITING_INVITE_TEXT = 'Waiting answer from `{}`...'
CANCEL_INVITE_TEXT = 'Okay, Bye!'
INVITE_REJECTED_TEXT = '{} rejected your request'
WRONG_ID_TEXT = 'Something\'s wrong. Please check that the ID is entered correctly'
WAIT_OPPONENT_MOVE_TEXT = 'Wait for the opponent move'
GAME_STARTED_TEXT = 'Game started. Your turn'
NOT_YOUR_TURN_TEXT = 'Its not your turn now, please wait for the opponent'
USER_MOVE_TEXT = '{} plays {}. Your turn'
INVALID_MOVE_TEXT = 'Invalid move, try again'
DRAW_TEXT = 'It is a stalemate position! Draw!'
WIN_TEXT = '{} won! Congratulations 🎉'
COMPUTER_MOVE = 'Computer Turn is {}'