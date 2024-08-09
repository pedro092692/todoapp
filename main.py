from flask import Flask, url_for, request, render_template
from dotenv import load_dotenv


# load env
load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():

    return 'hi pedro'


if __name__ == "__main__":
    app.run(debug=True)