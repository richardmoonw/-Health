from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/signup')
def sign_up():
	return render_template('sign_up.html')