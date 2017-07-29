from flaskblog import app
import os
import xlrd
from collections import OrderedDict
import simplejson as json
from flask import render_template, redirect, flash, url_for, session, request, jsonify
from blog.form import SetupForm, PostForm
from flaskblog import db, uploaded_images
import openpyxl
from werkzeug.utils import secure_filename
from pyexcel_xlsx import get_data
import json
from author.models import Author
from blog.models import Blog, Post, Category
from author.decorators import login_required, author_required
import bcrypt
from slugify import slugify 
from flask_uploads import UploadNotAllowed
from flask.ext import excel 
from flaskblog import dbmongo
import pymongo
from pymongo import MongoClient
POSTS_PER_PAGE = 5

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', blog=blog, posts=posts)

@app.route('/admin')
@app.route('/admin/<int:page>')
@login_required
@author_required
def admin(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/admin.html', posts=posts)


@app.route('/setup', methods=('GET', 'POST'))
def setup():
    
    blogs = Blog.query.count()
    if blogs:
        return redirect(url_for('admin'))
    form = SetupForm()
    if form.validate_on_submit():
       # import pdb;pdb.set_trace()
        salt = bcrypt.gensalt()
        mypassword = form.password.data.encode('utf-8')
        hashed_password = bcrypt.hashpw(mypassword, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True
        )
        db.session.add(author)
        db.session.flush()
        if author.id:
            blog = Blog(form.name.data, author.id)
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user"
        if author.id and blog.id:
            db.session.commit()
            flash('Blog created')
            return redirect(url_for('index'))
        else:
            db.session.rollback()
            error = "Error creating blog"
        
    return render_template('blog/setup.html', form=form)

@app.route('/post', methods=('GET', 'POST'))
@author_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        import pdb;pdb.set_trace()
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded")
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data
        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog, author, title, body, category, filename, slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
    return render_template('blog/post.html', form=form)
    
@app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)
    

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''
@app.route("/upload_to_mongo", methods=['GET', 'POST'])
def upload_to_mongo_file():
    if request.method == 'GET':
        data = get_data(os.path.join(app.config['UPLOAD_FOLDER'], "Book1.xlsx"))
        return json.dumps(data)

    
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_myfile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    
@app.route('/convert_to_json', methods=['GET', 'POST'])
def convert_to_json():    
    wb = xlrd.open_workbook(os.path.join(app.config['UPLOAD_FOLDER'], "Book1.xlsx"))
    sh = wb.sheet_by_index(0)
    c = MongoClient()
 
# List to hold dictionaries
    cars_list = []
 
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        cars = OrderedDict()
        row_values = sh.row_values(rownum)
        cars['car-id'] = row_values[0]
        cars['make'] = row_values[1]
        cars['model'] = row_values[2]
        cars['miles'] = row_values[3]
     
        cars_list.append(cars)
     
# Serialize the list of dicts to JSON
    j = json.dumps(cars_list)
    # create collection -bying
    # insert add j into the collection we created
    # Write to file
    c.test.biying.insert(j)

    
   # with open('data.json', 'w') as f:
        #f.write(j)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>'''