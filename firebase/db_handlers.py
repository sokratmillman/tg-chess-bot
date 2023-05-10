from firebase.db_init import database
from firebase.db_utils import *

def handle_game_request(uid_from, uid_to):
    database.update_user(uid=uid_from, changes_obj={
            "status": f'CONNECTING_WITH {uid_to}'
    })

    database.update_user(uid=uid_to, changes_obj={
        "status": f'CONNECTING_WITH {uid_from}'
    })

def handle_game_reject(uid_from, uid_to):
    database.update_user(uid=uid_from, changes_obj={
            "status": "AVAILABLE"
    })
    database.update_user(uid=uid_to, changes_obj={
            "status": "AVAILABLE"
    })

def handle_game_start(uid_from, uid_to):
    game_id = database.create_game(uid_from, uid_to)
    database.update_user(uid_from, {"status": "PLAYING", "current_game": game_id})
    database.update_user(uid_to, {"status": "PLAYING", "current_game": game_id})

def handle_draw_for_user(uid, partner_id="AI"):
    user_stats = database.get_user_stats(uid)
    user_draws = user_stats['draws']
    user_total_games = user_stats['total games']
    user_wins = user_stats['wins']
    user_losses = user_stats['losses']

    user_draws+=1
    user_total_games+=1
    user_ratio = user_wins/user_total_games

    new_stats = {
        "wins": user_wins,
        "losses": user_stats['losses'],
        "draws": user_draws,
        "total games": user_total_games,
        "% of wins": user_ratio
    }

    history = database.get_user_history(uid)
    new_history = generate_new_history(history, "draw", partner_id)

    database.update_user(uid, {"history": new_history, "stats": new_stats})

def handle_win_for_user(uid, partner_id="AI"):
    user_stats = database.get_user_stats(uid)
    user_draws = user_stats['draws']
    user_total_games = user_stats['total games']
    user_wins = user_stats['wins']
    user_losses = user_stats['losses']

    user_wins+=1
    user_total_games+=1
    user_ratio = user_wins/user_total_games

    new_stats = {
        "wins": user_wins,
        "losses": user_losses,
        "draws": user_draws,
        "total games": user_total_games,
        "% of wins": user_ratio
    }
    history = database.get_user_history(uid)
    new_history = generate_new_history(history, "win", partner_id)

    database.update_user(uid, {"history": new_history, "stats": new_stats})

def handle_loss_for_user(uid, partner_id="AI"):
    user_stats = database.get_user_stats(uid)
    user_draws = user_stats['draws']
    user_total_games = user_stats['total games']
    user_wins = user_stats['wins']
    user_losses = user_stats['losses']

    user_losses+=1
    user_total_games+=1
    user_ratio = user_wins/user_total_games

    new_stats = {
        "wins": user_wins,
        "losses": user_losses,
        "draws": user_draws,
        "total games": user_total_games,
        "% of wins": user_ratio
    }

    history = database.get_user_history(uid)
    new_history = generate_new_history(history, "loss", partner_id)

    database.update_user(uid, {"history": new_history, "stats": new_stats})

def handle_leaderboard_recalc():
    users = database.get_all_users()
    users_with_wins = dict(filter(lambda x: x[1]['stats']['wins'], users.items()))
    sorted_items = sorted(users_with_wins.items(), 
                          key=lambda x: x[1]['stats']['wins'], 
                          reverse=True)[:10]
    leaders = [item[0] for item in sorted_items]
    leaderboard = {f"{i+1}th": leaders[i] for i in range(len(leaders))}
    if len(leaderboard)>0:
        database.update_leaderboard(leaderboard)

def handle_pvp_finish(game_id, status, winner_color=None):
    game = database.get_game(game_id)

    black_uid = game['black']
    white_uid = game['white']

    if status=="draw":
        handle_draw_for_user(black_uid, white_uid)
        handle_draw_for_user(white_uid, black_uid)
    elif status=="canceled":
        # like no game was played
        pass
    elif status=="win":
        winner_id = black_uid if winner_color=="black" else white_uid
        loser_id = white_uid if winner_color=="black" else black_uid
        handle_win_for_user(winner_id, loser_id)
        handle_loss_for_user(loser_id, winner_id)

    database.update_user(black_uid, {"status": "AVAILABLE"})
    database.update_user(white_uid, {"status": "AVAILABLE"})

def handle_ai_finish(game_id, status, winner_color=None):
    game = database.get_game(game_id)

    player_uid = game['white']

    if status=='canceled':
        pass
    elif status=='draw':
        handle_draw_for_user(player_uid)
    elif status=='win':
        if winner_color=='white':
            handle_win_for_user(player_uid)
        else:
            handle_loss_for_user(player_uid)
    
    database.update_user(player_uid, {"status": "AVAILABLE"})

def handle_game_finish(game_id, status, type, winner_color=None):
    if type=="ai":
        handle_ai_finish(game_id, status, winner_color)
    elif type=="pvp":
        handle_pvp_finish(game_id, status, winner_color)

    handle_leaderboard_recalc()
