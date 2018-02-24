from wtforms import Form, IntegerField, StringField, validators
from flask_login import current_user

from bulls_and_cows.models import Game, Move, check_game_number
from bulls_and_cows.consts import MAXIMAL_BET, MINIMAL_WITHDRAWAL_AMOUNT


def load_game(game_id, fail_if_ended=True):
    game = Game.query.get(game_id)
    if game is None or current_user != game.player:
        return None, ['Game does not exist or cannot be accessed']
    if fail_if_ended and game.has_ended:
        return None, ['The game has already ended']
    return game, []


class NewMoveForm(Form):
    game_id = IntegerField(validators=[validators.DataRequired()])
    number = IntegerField(validators=[validators.DataRequired()])
    guess = StringField(validators=[lambda form, field: check_game_number(field.data)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move = None

    def validate(self):
        if not super().validate():
            return False

        game, errors = load_game(self.game_id.data)
        if errors:
            self.game_id.errors.extend(errors)
            return False

        last_move_number = game.moves[-1].number if game.moves else 0
        if self.number.data != last_move_number + 1:
            self.game_id.errors.append('Incorrect move number, expected {}'
                                       .format(last_move_number + 1))
            return False

        self.move = Move(
            game=game,
            number=self.number.data,
            guess=self.guess.data)
        return True


class EndGameForm(Form):
    game_id = IntegerField(validators=[validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None

    def validate(self):
        if not super().validate():
            return False

        self.game, errors = load_game(self.game_id.data)
        self.game_id.errors.extend(errors)
        return not errors


class NewGameForm(Form):
    bet = IntegerField(validators=[validators.number_range(min=1, max=MAXIMAL_BET)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None

    def validate(self):
        if not super().validate():
            return False

        if self.bet.data > current_user.balance:
            self.bet.errors.append('The bet cannot be greater than the balance')
            return False

        self.game = Game(bet=self.bet.data, player=current_user)
        return True


class WithdrawMoneyForm(Form):
    amount = IntegerField(validators=[validators.number_range(min=MINIMAL_WITHDRAWAL_AMOUNT)])

    def validate(self):
        if not super().validate():
            return False

        if current_user.balance < self.amount.data:
            self.amount.errors.append('You cannot withdraw more than you have')
            return False

        return True
