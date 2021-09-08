from flask import Flask

app = Flask(__name__)

app.config['FLASK_APP']='main'
app.config['FLASK_ENV']='development'
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True

from app import routes
