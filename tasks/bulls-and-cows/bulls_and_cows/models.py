import string
import random
import math

from flask_sqlalchemy import SQLAlchemy

from bulls_and_cows.consts import INITIAL_BALANCE


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    games = db.relationship('Game', back_populates='player', order_by='Game.id')
    balance = db.Column(db.Integer, nullable=False, default=INITIAL_BALANCE, server_default=str(INITIAL_BALANCE))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


def generate_game_number():
    return ''.join(random.sample(string.digits, 4))


def is_game_number_correct(digits):
    return (
        len(digits) == 4 and
        len(set(digits)) == 4 and
        set(digits) < set(string.digits)
    )


def check_game_number(digits):
    if not is_game_number_correct(digits):
        raise ValueError('Invalid game number')


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    bet = db.Column(db.Integer, nullable=False)
    secret_number = db.Column(db.String(4), nullable=False)
    has_ended = db.Column(db.Boolean, nullable=False, default=False, server_default='false')

    player = db.relationship('User', back_populates='games')
    moves = db.relationship('Move', back_populates='game', order_by='Move.number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.secret_number is None:
            self.secret_number = generate_game_number()
        check_game_number(self.secret_number)

        if self.bet <= 0:
            raise ValueError('The bet should be positive')

    def has_player_won(self):
        return any(move.bulls() == 4 for move in self.moves)

    def payoff_multiplier(self, number_of_moves):
        if number_of_moves >= 9:
            return 0
        elif number_of_moves == 8:
            return 0.25
        elif number_of_moves == 7:
            return 0.5
        elif number_of_moves == 6:
            return 2
        else:
            return 3

    def end(self):
        self.has_ended = True
        bet_multiplier = -1  # Withdraw the bet
        if self.has_player_won():
            bet_multiplier += self.payoff_multiplier(len(self.moves))
        balance_change = int(math.floor(self.bet * bet_multiplier))
        self.player.balance = User.balance + balance_change


class Move(db.Model):
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id, ondelete='CASCADE'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    guess = db.Column(db.String(4), nullable=False)

    game = db.relationship('Game', back_populates='moves')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        check_game_number(self.guess)

    def bulls(self):
        return sum(1 for secret_digit, guessed_digit
                   in zip(self.game.secret_number, self.guess)
                   if secret_digit == guessed_digit)

    def cows(self):
        return len(set(self.guess) & set(self.game.secret_number)) - self.bulls()
