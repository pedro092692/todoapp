from flask import Flask, url_for, request, render_template, redirect
from dotenv import load_dotenv
from turbo_flask import Turbo
from flask_security import login_required, current_user
from database import DataBase
import os


# load env
load_dotenv()

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Turbo flask
turbo = Turbo(app)

# flask security
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

# database
db = DataBase(app)
db.create_tables()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)