import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import chess

class MyDatabase:
    def __init__(self, cred_path, db_URL):
        creds = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(creds, options={
            'databaseURL':  db_URL,
        })

        current_users = db.reference().child("users").get()
        current_games = db.reference().child("active_games").get()
        current_leaders = db.reference().child("leaderboard").get()

        db.reference().set({
            'users': current_users,
            'active_games': current_games,
            'leaderboard': current_leaders,
        })

        db.reference().child('users').update({
            "0": {
                'history': '',
                'status': 'AVAILABLE',
                'current_game': '-1',
                'stats': {
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'total games': 0,
                    '% of wins': 0,
                }
            }
        })
        
        self.USERS = db.reference("users")
        self.ACTIVE_GAMES = db.reference("active_games")
        self.LEADERBOARD = db.reference("leaderboard")

    def reset(self):
        db.reference().set({
            'users': {},
            'active_games': {},
            'leaderboard': {}
        })
    
    def get_all_users(self):
        return self.USERS.get()
    
    def create_user(self, uid):
        ref = self.USERS
        if ref.child(str(uid)).get() is None:
            ref.update({str(uid):{
                'history': '',
                'status': 'AVAILABLE',
                'current_game': '-1',
                'stats': {
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'total games': 0,
                    '% of wins': 0,
                }
            }})
    
    def update_user(self, uid, changes_obj):
        ref = self.USERS.child(str(uid))
        if ref.get() is None:
            return
        ref.update(changes_obj)

    def get_user(self, uid):
        ref = self.USERS.child(str(uid))
        return ref.get()
    
    def create_game(self, uid_from, uid_to):
        ref = self.ACTIVE_GAMES
        board_str = chess.Board().fen()
        game_id_ref = ref.push()
        game_id_ref.set({
            'white': str(uid_from),
            'black': str(uid_to),
            'current_turn': uid_from,
            'board': board_str,
        })

        game_id = game_id_ref.key
        return game_id
    
    def update_game(self, game_id, changes_obj):
        ref = self.ACTIVE_GAMES.child(game_id)
        if ref.get() is None:
            return
        ref.update(changes_obj)
    
    def get_game(self, game_id):
        ref = self.ACTIVE_GAMES.child(game_id)
        return ref.get()
    
    def get_all_games(self):
        return self.ACTIVE_GAMES.get()

    def delete_game(self, game_id):
        ref = self.ACTIVE_GAMES.child(game_id)
        ref.delete()
    
    def init_leaderboard(self, first_leader, second_leader=None):
        ref = self.LEADERBOARD
        ref.update({"1st": first_leader} if second_leader is None else {"1st": first_leader, "2nd":second_leader})
    
    def update_leaderboard(self, changes_obj):
        ref = self.LEADERBOARD
        ref.update(changes_obj)

    def get_leaderboard(self):
        return self.LEADERBOARD.get()
    
    def get_user_stats(self, uid):
        return self.get_user(uid)['stats']
    
    def get_user_history(self, uid):
        return self.get_user(uid)['history']
    