import sys
sys.path.insert(0, '/var/www/ops-record')

activate_this = '#location of the virtual environment identified earlier/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application #move this file (app.wsgi) to the server folder