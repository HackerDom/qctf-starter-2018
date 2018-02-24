import re
import json
import logging
from app import app
from flask import render_template

ID_PATTERN = re.compile(r'^[a-z0-9]+$')
with open('flags.json') as file:
    FLAGS = json.load(file)
app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)


@app.route('/<team_id>')
def team_index(team_id):
    app.logger.info(f'Request /{team_id}')
    if not id_is_valid(team_id):
        return "Team id is not valid", 404
    return render_template('index.html', team_id=team_id)


@app.route('/flag_request/<team_id>')
def flag_request(team_id):
    app.logger.info(f'Request /flag_request/{team_id}')
    if not id_is_valid(team_id):
        return "Team id is not valid", 404
    return render_template('request.html'), {'Refresh': f'5;url=/get_flag/{team_id}'}


@app.route('/get_flag/<team_id>')
def get_flag(team_id):
    app.logger.info(f'Request /get_flag/{team_id}')
    if not id_is_valid(team_id):
        return "Team id is not valid", 404
    return list(filter(lambda dic: dic['team_id'] == team_id, FLAGS))[0]['flag'], 302, {'Location': f'/{team_id}'}


@app.route('/')
def index():
    return "Team id is not valid", 404


def id_is_valid(team_id):
    if not re.fullmatch(ID_PATTERN, team_id) or \
            len(list(filter(lambda dic: dic['team_id'] == team_id, FLAGS))) == 0:
        app.logger.info(f'Aborted, invalid id: {team_id}')
        return False
    return True


if __name__ == '__main__':
    app.run()
