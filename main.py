from flask import Flask, url_for, request, render_template, redirect
from dotenv import load_dotenv
from turbo_flask import Turbo
from flask_security import login_required, current_user
from database import DataBase, Task
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
@login_required
def home():
    if request.method == 'POST':
        task_title = request.form.get('task_title')

        new_task = Task.create_task(
            user_id=current_user.id,
            title=task_title
        )

        if len(current_user.tasks) > 1:
            return add_task(template='_task-item.html', target='task-list', method='prepend', task=new_task)

        else:
            return add_task(template='_first_task.html', target='task-container', method='replace', task=None)

    return render_template('index.html')




@app.route('/login')
def login():
    return render_template('security/login_user.html')


@app.route('/register')
def register():
    return render_template('security/register_user.html')


def add_task(template, target, method, task):
    """
    :param str template this is the template to be render:
    :param str target the target where turbo replace update or remove :
    :param str method turbo flask method:
    :param object task is it needed task object will be render in the template:
    :return: a render of part the template without refreshing all page.
    """
    _method = getattr(turbo, method)
    if turbo.can_stream():
        return turbo.stream(
            _method(render_template(f'includes/{template}', task=task), target=target)
        )


if __name__ == "__main__":
    app.run(debug=True)
