from flask import Flask, url_for, request, render_template, redirect
from dotenv import load_dotenv
from turbo_flask import Turbo
import time
import threading


# load env
load_dotenv()

app = Flask(__name__)

# Turbo flask
turbo = Turbo(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    number = 0
    if request.method == 'POST':
        number = request.form.get('number')
    if turbo.can_stream():
        print('hi pedro')
        print(number)
        return turbo.stream(
            turbo.update(render_template('includes/number.html', number=number), target='number')
        )


    return render_template('index.html', number=number)

@app.route('/some')
def some():
    return 'some'


if __name__ == "__main__":
    app.run(debug=True)