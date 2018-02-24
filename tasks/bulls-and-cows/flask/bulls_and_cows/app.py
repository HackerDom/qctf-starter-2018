import os

from flask import Flask, render_template, url_for, redirect, jsonify
from flask_login import LoginManager, login_required, login_user, current_user

from bulls_and_cows.models import db, User
from bulls_and_cows.forms import NewMoveForm, EndGameForm, NewGameForm, WithdrawMoneyForm, load_game
from bulls_and_cows.schemas import GameSchema, UserSchema
from bulls_and_cows.utils import validate_form, dump_with_empty_errors


app = Flask(__name__)
app.config.from_object('bulls_and_cows.default_config')
if os.getenv('ENVIRONMENT') == 'DEV':
    app.config.from_object('bulls_and_cows.development_config')
else:
    app.config.from_envvar('APP_CONFIG')

with app.app_context():
    db.init_app(app)
    login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def autoregister():
    if not current_user.is_authenticated:
        new_user = User()
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/me', methods=['GET'])
@login_required
def me():
    return dump_with_empty_errors('me', current_user, UserSchema())


@app.route('/games/<game_id>', methods=['GET'])
@login_required
def game(game_id):
    game, errors = load_game(game_id, fail_if_ended=False)
    if errors:
        return jsonify({'errors': errors}), 403

    return dump_with_empty_errors('game', game, GameSchema())


@app.route('/games', methods=['POST'])
@login_required
@validate_form(NewGameForm)
def new_game(form):
    db.session.add(form.game)
    db.session.commit()
    return redirect(url_for('game', game_id=form.game.id))


@app.route('/end_game', methods=['POST'])
@login_required
@validate_form(EndGameForm)
def end_game(form):
    form.game.end()
    db.session.commit()
    return redirect(url_for('me'))


@app.route('/move', methods=['POST'])
@login_required
@validate_form(NewMoveForm)
def new_move(form):
    db.session.add(form.move)
    if form.move.bulls() == 4:
        form.move.game.end()
    db.session.commit()
    if form.move.game.has_ended:
        return redirect(url_for('me'))
    return redirect(url_for('game', game_id=form.move.game_id))


@app.route('/withdraw', methods=['POST'])
@login_required
@validate_form(WithdrawMoneyForm)
def withdraw(form):
    current_user.balance = User.balance - form.amount.data
    current_user.has_withdrawn = True
    db.session.commit()
    return redirect(url_for('me'))


if __name__ == '__main__':
    app.run()
