from functools import wraps

from flask import request, jsonify


def validate_form(form_class):
    def decorator(func):
        @wraps(func)
        def decorated():
            form = form_class(request.form)
            if form.validate():
                return func(form)

            all_errors = sum(form.errors.values(), [])
            return jsonify({'errors': all_errors}), 403

        return decorated

    return decorator
