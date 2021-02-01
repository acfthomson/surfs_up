# Import dependency
from flask import Flask

# Create a Flask instance
app = Flask(__name__)

# Create a route
@app.route('/')
def hello_world():
    return 'Hello world'
