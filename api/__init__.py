from flask             import Flask
from flask_mail        import Mail
from flask_bcrypt      import Bcrypt
from flask_mongoengine import MongoEngine

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

mail = Mail()
mail.init_app(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

from api import routes
