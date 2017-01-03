# Set the path
import os, sys
print ("before{0}".format(sys.path))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print ("after{0}".format(sys.path))

from flask_script import Manager, Server

from flask_celery_example import app
from flask_celery_example import celery
from flask_celery_example import views
manager = Manager(app)




# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()
