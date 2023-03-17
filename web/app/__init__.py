import os

from flask import Flask
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_uploads import UploadSet, IMAGES, configure_uploads



app = Flask(__name__, static_folder='static')
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
images = UploadSet('photos', IMAGES)
configure_uploads(app, images)

# this DEBUG config here will be overridden by FLASK_DEBUG shell environmentapp.config['DEBUG'] = True 
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'bb2b94bb79773c71f94a310327f9d118aa78201156c726bf' 
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID", None)
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET", None)
app.config['GOOGLE_DISCOVERY_URL'] = os.getenv("GOOGLE_DISCOVERY_URL", None)
app.config['FACEBOOK_CLIENT_ID'] = os.getenv("FACEBOOK_CLIENT_ID", None)
app.config['FACEBOOK_CLIENT_SECRET'] = os.getenv("FACEBOOK_CLIENT_SECRET", None)

if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
oauth = OAuth(app)
login_manager = LoginManager()
login_manager.login_view = 'freeFan_login'
login_manager.init_app(app)

from app import views  # noqa   #do not move the position of this import
