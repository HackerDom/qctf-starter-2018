import pickle
from math import ceil

from flask import Flask, request, jsonify

import db
import features


with open('model.pickle', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/submit_credit_form', methods=['POST'])
def submit_credit_form():
    fdict = features.form_to_feature_dict(request.form)
    farray = features.feature_dict_to_array(fdict)
    interest = round(model.predict([farray])[0], 3)

    if interest >= 1.50:
        return jsonify({'result': 'negative'})

    duration = fdict['duration']
    bank_asks = fdict['credit_amount'] * interest ** duration
    monthly_payment = ceil(bank_asks / (12 * duration))
    flag = db.save_and_get_code(fdict, interest)

    return jsonify({
        'result': 'positive',
        'interest_rate': str(round((interest - 1) * 100, 1)),
        'monthly_payment': monthly_payment,
        'bank_code': flag,
    })
