import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)