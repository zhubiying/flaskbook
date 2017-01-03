from flask_celery_example import app
from flask import render_template, redirect, flash, url_for, session, request
from flask_celery_example import celery
from flask import jsonify
from tasks import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    msg = Message('Hello from Flask',
                  recipients=[request.form['email']])
    msg.body = 'This is a test email sent from a background Celery task.'
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email(msg)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.delay()
    app.logger.debug("result backend {0}".format(task.backend))
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    app.logger.debug("task status. {0} {1}".format(task.state, task_id))
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
   app.debug = True
   app.secret_key = '\x17\xd4\xfe\x08\xa0\x9a\x8f~\x1d\x8eG\xc4\xfc85\xefP\x08\xbc\x90O\x14*\x8a'
    # logging
   log = r'/home/ubuntu/myapp'
   if not os.path.exists(log):
       os.makedirs(log)    
   handler = RotatingFileHandler(os.path.join(log, 'error.log'), maxBytes=10000, backupCount=5)
   handler.setLevel(logging.INFO)
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   handler.setFormatter(formatter)
   app.logger.addHandler(handler)    
   app.run(app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5000))))
