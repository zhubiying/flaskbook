from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
import sys
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks import *
app = Flask(__name__)
app.config.from_object('settings')
celery = make_celery(app)

db = SQLAlchemy(app)
# migrations
migrate = Migrate(app, db)

# markdown
md = Markdown(app, extensions=['fenced_code', 'tables'])

# images
uploaded_images = UploadSet('images', IMAGES)
configure_uploads(app, uploaded_images)

from blog import views
from author import views

