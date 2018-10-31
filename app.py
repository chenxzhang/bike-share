import draft
from flask import Flask
import pygeodesy
app = Flask(__name__)

@app.route('/')
def hello_world():
    return draft.readCSVSkipOneLine2(bike_data.csv)
