import draft
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
    #return str(draft.number_of_regulars("bike_data.csv"))

@app.route('/user/<chen>')
def show_user_profile(chen):
    # show the user profile for that user
    return 'User %s' % "chen"

@app.route('/images')
def show_post():
    # show the post with the given id, the id is an integer
    return 'Post %d' % 32