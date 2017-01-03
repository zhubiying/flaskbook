import os

SECRET_KEY = 'you-will-never-guess'
DEBUG=True

# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_BACKEND = 'redis://localhost:6379'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'flask@example.com'


CELERY_BROKER_URL = 'amqp://zedekiah:auc753@localhost:5672/flask_celery_example'
CELERY_RESULT_BACKEND = 'amqp'
CELERYD_STATE_DB = "/opt/path/data/celery_worker_state"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False