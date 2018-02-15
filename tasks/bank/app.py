from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/submit_credit_form', methods=['POST'])
def submit_credit_form():
    print(request.form)
    return jsonify({
        'result': 'positive',
        'interest_rate': 15,
        'monthly-payment': 30000,
        'bank_code': 'QCTF_KEK',
    })
