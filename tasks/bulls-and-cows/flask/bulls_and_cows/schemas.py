from marshmallow import Schema, fields, missing


class MoveSchema(Schema):
    number = fields.Int()
    guess = fields.Str()
    bulls = fields.Function(lambda move: move.bulls())
    cows = fields.Function(lambda move: move.cows())


class GameSchema(Schema):
    id = fields.Int()
    bet = fields.Int()
    has_ended = fields.Bool()
    secret_number = fields.Function(lambda game: game.secret_number if game.has_ended else missing)
    moves = fields.Nested(MoveSchema, many=True)


class UserSchema(Schema):
    balance = fields.Int()
    codes = fields.Function(lambda obj: obj.codes())
    games = fields.Nested(GameSchema, many=True)
