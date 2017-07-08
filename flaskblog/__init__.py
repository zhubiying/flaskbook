from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from flask_mongoengine import MongoEngine
import sys
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
app = Flask(__name__)
app.config.from_object('settings')


db = SQLAlchemy(app)
dbmongo = MongoEngine()
# migrations
migrate = Migrate(app, db)

# markdown
md = Markdown(app, extensions=['fenced_code', 'tables'])

# images
uploaded_images = UploadSet('images', IMAGES)
configure_uploads(app, uploaded_images)
from author import views
from blog import  views


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])