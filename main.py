from flask import Flask, url_for, request, render_template
from dotenv import load_dotenv


# load env
load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)