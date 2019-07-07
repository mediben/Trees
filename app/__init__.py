import sys
from config import Config
from flask import Flask, render_template
from tree import tree

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(tree)

@app.route('/')
def index():
    return render_template('node.html')

