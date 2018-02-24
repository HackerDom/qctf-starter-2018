from os.path import dirname, join
import os

def getenv(variable_name):
    value = os.getenv(variable_name, None)
    if value is None:
        raise ValueError('Please specify the "{}" environment variable'
                         .format(variable_name))
    return value

db_config = dict(
    host='db',
    user='root',
    passwd=getenv('MYSQL_ROOT_PASSWORD'),
    db='qctfminer',
    charset='utf8'
)

aplication_config = dict(
    cookie_secret='w9R9Y7/wQIC9MF21PHc+DVH8mxkNykWNimojniV/j8o=',
    static_path=join(dirname(__file__), "static"),
    template_path=join(dirname(__file__), "templates")
)
