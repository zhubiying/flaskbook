import os

SECRET_KEY = 'you-will-never-guess'
DEBUG=True
DB_USERNAME = 'zedekiah'
DB_PASSWORD = '' # not required for cloud9
BLOG_DATABASE_NAME = 'blog'
DB_HOST = os.getenv('IP', '0.0.0.0')
DB_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
UPLOADED_IMAGES_DEST = '/home/ubuntu/workspace/flaskblog/static/images'
UPLOADED_IMAGES_URL = '/static/images/'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_BACKEND = 'redis://localhost:6379'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'flask@example.com'