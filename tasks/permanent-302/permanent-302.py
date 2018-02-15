import re
import json
from app import app
from flask import render_template, abort

ID_PATTERN = re.compile(r'^[a-f0-9]+$')
with open('flags.json') as file:
    FLAGS = json.load(file)


@app.route('/<team_id>')
def index(team_id):
    validate_id(team_id)
    return render_template('index.html', team_id=team_id)


@app.route('/flag_request/<team_id>')
def flag_request(team_id):
    validate_id(team_id)
    return render_template('request.html'), {'Refresh': f'5;url=/get_flag/{team_id}'}


@app.route('/get_flag/<team_id>')
def get_flag(team_id):
    validate_id(team_id)
    return FLAGS[team_id], 302, {'Location': f'/{team_id}'}


def validate_id(team_id):
    if not re.fullmatch(ID_PATTERN, team_id):
        abort(404)
    if team_id not in FLAGS.keys():
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
