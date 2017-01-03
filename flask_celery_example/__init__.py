from flask import Flask
import sys
import os
import random
import time
from celery import Celery
app = Flask(__name__)
app.config.from_object('settings')


# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.config_from_object('settings')
app.config['CELERY_BROKER_URL'] = 'amqp://zedekiah:auc753@localhost:5672/flask_celery_example'
app.config['CELERY_RESULT_BACKEND'] = 'amqp'
app.config['CELERYD_STATE_DB'] = "/opt/path/data/celery_worker_state"
app.config['CELERY_ACCEPT_CONTENT'] = ['json']
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_RESULT_SERIALIZER'] = 'json'
app.config['CELERY_IGNORE_RESULT'] = False

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from flask.ext.mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
mail = Mail(app)