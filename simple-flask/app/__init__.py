from flask import Flask

app = Flask(__name__)

# Load the configuration from config.py
app.config.from_pyfile('../config.py')
app.template_folder = app.config['TEMPLATES_FOLDER']

# Import the views and models modules
from app import views