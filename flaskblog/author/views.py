from flaskblog import app
from flask import render_template, redirect, flash, url_for, session, request
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt
from flask import jsonify


  

@app.route('/indexes')
def indexes():
    return render_template('indexes.html')

if __name__ == '__main__':
    app.run()
    
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    app.logger.debug('login form')
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(
            username=form.username.data,
            ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                # flash(fib.delay(25))
                flash("User {0} logged in ".format(form.username.data))
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = "Incorrect password"
        else:
            error = "Author not found"
    return render_template('author/login.html', form=form, error=error)



@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('author/register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    flash('User logged out')
    return redirect(url_for('index'))

@app.route('/success')
def success():
    return "Author registered!"

@app.route('/login_success')
@login_required
def login_success():
    return "Author logged in!"