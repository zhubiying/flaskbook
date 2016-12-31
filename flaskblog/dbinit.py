# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flaskblog import app
import sqlalchemy

db_uri = 'mysql+pymysql://{0}:{1}@{2}/'.format(app.config['DB_USERNAME'], app.config['DB_PASSWORD'], app.config['DB_HOST'])
engine = sqlalchemy.create_engine(db_uri)
conn = engine.connect()
conn.execute("commit")
conn.execute("drop database "  + app.config['BLOG_DATABASE_NAME'])
conn.execute("create database "  + app.config['BLOG_DATABASE_NAME'])
conn.close()
