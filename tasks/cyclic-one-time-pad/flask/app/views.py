import os
from base64 import b64encode, b64decode

from flask import render_template, flash, redirect
from app import app
from app.forms import EncryptForm
from app.cipher import CipherProvider

@app.route('/')
@app.route('/encrypt', methods = ['GET', 'POST'])
def encrypt():
    form = EncryptForm()
    app.logger.info(form.data_format.data)
    if form.validate_on_submit():
        try:
            raw_data = form.data.data.encode()
            if form.data_format.data == 'plain':
                data = raw_data
            elif form.data_format.data == 'base64':
                try:
                    data = b64decode(raw_data)
                except Exception as e:
                    flash('Входные данные не являются валидным base64')
                    return render_template('encrypt.html', form=form, active='encrypt')
            else:
                raise Exception('Form is empty')
        except Exception as e:
            flash('Произошла ошибка')
            app.logger.info("Exception while parsing data: {}".format(e))
            return render_template('encrypt.html', form=form, active='encrypt')

        cipher = CipherProvider.get_cipher(app.config["CIPHER_GLOBAL_SEED"], app.config["CIPHER_KEY_LEN"])
        encrypted = cipher.encrypt(data)
        plain = encrypted
        base64 = b64encode(encrypted).decode()
        return render_template('result.html', plain=plain, base64=base64)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Error in the {} field - {}".format(getattr(form, field).label.text, error))
    return render_template('encrypt.html', form=form, active='encrypt')

@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html', active='decrypt')

@app.route('/about')
def about():
    return render_template('about.html', active='about')
