from marshmallow import Schema, fields


class MoveSchema(Schema):
    number = fields.Int()
    guess = fields.Str()
    bulls = fields.Function(lambda obj: obj.bulls())
    cows = fields.Function(lambda obj: obj.cows())


class GameSchema(Schema):
    id = fields.Int()
    bet = fields.Int()
    has_ended = fields.Bool()
    moves = fields.Nested(MoveSchema, many=True)


class UserSchema(Schema):
    balance = fields.Int()
    games = fields.Nested(GameSchema, many=True)
