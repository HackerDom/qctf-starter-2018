from functools import wraps

from flask import request, jsonify


def validate_form(form_class):
    def decorator(func):
        @wraps(func)
        def decorated():
            form = form_class(request.form)
            if form.validate():
                return func(form)
            return jsonify({'errors': form.errors}), 403

        return decorated
    return decorator


def dump_with_empty_errors(key, value, value_schema):
    return jsonify({
        'errors': [],
        key: value_schema.dump(value).data
    })
