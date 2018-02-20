from flask import Flask
from flask_login import LoginManager
import generate_dirs

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

generate_dirs.generate(app.config['USERS_FILE'], app.config['USER_DATA_DIR'], app.config['FAKE_USERS'])

from app import views
