from flask import Flask, url_for, request, render_template, redirect
from dotenv import load_dotenv
from turbo_flask import Turbo
from flask_security import login_required, current_user
from database import DataBase, Task, SubTask
import os


# load env
load_dotenv()

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# humanize date in jinja2
# pip install jinja2-humanize-extension
app.jinja_options['extensions'] = ['jinja2_humanize_extension.HumanizeExtension']

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
    # completed task
    completed = get_user_completed_task()

    # add task
    if request.method == 'POST' and 'add-form' in request.form:
        task_title = request.form.get('task')
        new_task = Task.create_task(
            user_id=current_user.id,
            title=task_title
        )

        if len(current_user.tasks) > 1:
            return render_frame(template='_task-item.html', target='task-list', method='prepend', content=new_task)

        else:
            completed = get_user_completed_task()
            return render_frame(template='_first_task.html', target='task-container', method='replace', content=completed)
    # search task
    if request.method == 'POST' and 'search-form' in request.form:
        query = request.form.get('search')
        user_task = Task.search(user_id=current_user.id, query=query)

        if turbo.can_stream():
            if query != '':
                return turbo.stream([
                    turbo.update(render_template('includes/_task_list.html', content=user_task), target='task-list'),
                    turbo.remove(target='completed')
                ])
            else:
                return render_frame(template='_first_task.html', target='task-container', method='replace', content=None)
    # show task detail
    if request.method == 'POST' and 'task-id' in request.form:
        task_id = request.form.get('task-id')
        task = Task.get_task(task_id)
        return render_frame(template='_more_info.html', target='more-info', method='update', content=task)

    # add task step
    if request.method == 'POST' and 'add-step-form' in request.form:
        task_id = request.form.get('task_id')
        title = request.form.get('step')
        new_step = SubTask.add_step(
            task_id=task_id,
            title=title
        )
        return render_frame(template='_step_item.html', target='task-steps', method='prepend', content=new_step)

    # complete task

    if request.method == 'POST' and 'task-check' in request.form:
        task_id = request.form.get('task-check')
        task = Task.get_task(task_id=task_id)
        Task.edit_task(task=task)
        completed = get_user_completed_task()
        if turbo.can_stream():
            return turbo.stream([
                turbo.remove(target=f'task-item-container-{task_id}'),
                turbo.replace(render_template('includes/_completed_number.html', completed_task=completed),
                              target='completed-number'),
                turbo.append(render_template('includes/_completed_task.html', content=task), target='completed-list')
            ])

    return render_template('index.html', completed_task=completed)




@app.route('/login')
def login():
    return render_template('security/login_user.html')


@app.route('/register')
def register():
    return render_template('security/register_user.html')


def render_frame(template, target, method, content, ):
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
            _method(render_template(f'includes/{template}', content=content), target=target)
        )


def get_user_completed_task():
    """
    This function return the number (int) of current user completed task.
    :return:
    """
    return Task.count_completed(user_id=current_user.id)

if __name__ == "__main__":
    app.run(debug=True)
