import data_analysis
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def webapp():
    return render_template('index.html')
