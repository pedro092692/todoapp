from flask import Flask, url_for, request, render_template, redirect, flash
from dotenv import load_dotenv
from turbo_flask import Turbo
from flask_security import login_required, current_user, verify_password, hash_password
from database import DataBase, Task, SubTask, User, Checklist
from werkzeug.security import check_password_hash
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
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/login'

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
        task_title = request.form.get('task').lstrip()
        if task_title:
            new_task = Task.create_task(
                user_id=current_user.id,
                title=task_title
            )
            if len(current_user.tasks) > 1:
                return render_frame(template='_task-item.html', target='task-list', method='prepend', content=new_task)

            else:
                return redirect(url_for('home'))
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
                return redirect(url_for('home'))
    # show task detail
    if request.method == 'POST' and 'task-id' in request.form:
        task_id = request.form.get('task-id')
        task = Task.get_task(task_id)
        return render_frame(template='_more_info.html', target='more-info', method='update', content=task)
    # add task step
    if request.method == 'POST' and 'add-step-form' in request.form:
        task_id = request.form.get('task_id')
        title = request.form.get('step')
        if title:
            new_step = SubTask.add_step(
                task_id=task_id,
                title=title
            )
            task_parent = Task.get_task(task_id=task_id)
            return render_frame(template='_more_info.html', target='more-info', method='update', content=task_parent)
    # complete task
    if request.method == 'POST' and 'task-check' in request.form:
        task_id = request.form.get('task-check')
        task = Task.get_task(task_id=task_id)
        if task.completed:
            Task.uncompleted_task(task)
            completed = get_user_completed_task()
            if turbo.can_stream():
                return turbo.stream([
                    turbo.remove(target=f'completed-task-{task_id}'),
                    turbo.replace(render_template('includes/_completed_number.html', completed_task=completed),
                                  target='completed-number'),
                    turbo.prepend(render_template('includes/_task-item.html', content=task), target='task-list'),
                    # if the more info panel if open
                    turbo.update(render_template('includes/_more_info.html', content=task), target='more-info')
                ])
        else:
            Task.completed_task(task=task)
            completed = get_user_completed_task()
            if turbo.can_stream():
                return turbo.stream([
                    turbo.remove(target=f'task-item-container-{task_id}'),
                    turbo.replace(render_template('includes/_completed_number.html', completed_task=completed),
                                  target='completed-number'),
                    turbo.prepend(render_template('includes/_completed_task.html', content=task), target='completed-list'),
                    # if the more info panel if open
                    turbo.update(render_template('includes/_more_info.html', content=task), target='more-info')
                ])
    # edit task title
    if request.method == 'POST' and 'task-title-edit' in request.form:
        task_title = request.form.get('task-title-edit')
        task_id = request.form.get('task-id-edit')
        edited_task = Task.get_task(task_id=task_id)
        if task_title:
            task = Task.get_task(task_id=task_id)
            edited_task = Task.edit_task_title(task=task, title=task_title)
            if turbo.can_stream():
                    if not task.completed:
                        return turbo.stream([
                            turbo.update(render_template('includes/_more_info.html', content=edited_task), target='more-info'),
                            turbo.replace(render_template('includes/_task-item.html', content=task),
                                          target=f'task-item-container-{task_id}')
                        ])
                    else:
                        return turbo.stream([
                            turbo.update(render_template('includes/_more_info.html', content=edited_task), target='more-info'),
                            turbo.replace(render_template('includes/_completed_task.html', content=task),
                                          target=f'completed-task-{task_id}')
                        ])
        return render_frame(template='_more_info.html', target='more-info', method='update', content=edited_task)
    # completed subtask
    if request.method == 'POST' and 'subtask-id' in request.form:
        subtask_id = request.form.get('subtask-id')
        subtask = SubTask.get_subtask(subtask_id=subtask_id)
        parent_task = Task.get_task(task_id=subtask.task_id)
        if subtask.completed:
            Task.uncompleted_task(subtask)
        else:
            Task.completed_task(subtask)
        return render_frame(template='_more_info.html', target='more-info', method='update', content=parent_task)
    # edit subtask title
    if request.method == 'POST' and 'task-id-edit' in request.form:
        subtask_id = request.form.get('task-id-edit')
        title = request.form.get('subtask-edited-name')
        subtask = SubTask.get_subtask(subtask_id=subtask_id)
        task = Task.get_task(task_id=subtask.task_id)
        if title:
            Task.edit_task_title(subtask, title=title)
        return render_frame(template='_more_info.html', target='more-info', method='update', content=task)
    # delete task
    if request.method == 'POST' and 'task-id-delete' in request.form:
        task_id = request.form.get('task-id-delete')
        task = Task.get_task(task_id=task_id)
        Task.delete_task(task)
        if task.completed:
            if turbo.can_stream():
                completed = get_user_completed_task()
                if completed > 0:
                    return turbo.stream([
                            turbo.remove(target=f'completed-task-{task_id}'),
                            turbo.replace(render_template('includes/_completed_number.html', completed_task=completed),
                                      target='completed-number')
                        ]
                    )
                else:
                    return redirect(url_for('home'))
        else:
            if turbo.can_stream():
                if completed > 0:
                    return turbo.stream(
                        turbo.remove(target=f'task-item-container-{task_id}')
                    )
                else:
                    return redirect(url_for('home'))

    return render_template('index.html', completed_task=completed)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('security/login_user.html')


@app.route('/register')
def register():
    return render_template('security/register_user.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if verify_password(password=current_password, password_hash=current_user.password) and new_password:
            User.update_password(current_user, hash_password(new_password))
            flash('your password has been changed.')
        else:
            flash('invalid password.')

    return render_template('profile.html')


@app.route('/checklist', methods=['GET', 'POST'])
@login_required
def checklist():
    # completed list item
    completed_items = Checklist.get_completed_items(user_id=current_user.id)
    if request.method == 'POST' and 'item-id' in request.form:
        item_id = request.form.get('item-id')
        item = Checklist.get_item(item_id=item_id)
        Checklist.completed_item(item)
        completed_items = Checklist.get_completed_items(user_id=current_user.id)
        return render_frame(template='_checklist_update.html', target='checklist-content', method='replace',
                            content=completed_items)
    # add item to checklist
    if request.method == 'POST' and 'item-name' in request.form:
        item_name = request.form.get('item-check')
        if item_name:
            user_checklist = current_user.checklist
            new_item = Checklist.add_new_item(item_name=item_name, user_id=current_user.id)

            return render_frame(template='_checklist_update.html', target='checklist-content', method='replace',
                                    content=completed_items)
    # uncompleted item
    if request.method == 'POST' and 'item-id-completed' in request.form:
        item_id = request.form.get('item-id-completed')
        item = Checklist.get_item(item_id=item_id)
        Checklist.completed_item(item, completed=False)
        return render_frame(template='_checklist_update.html', target='checklist-content', method='replace',
                                    content=Checklist.get_completed_items(user_id=current_user.id))
    # delete all completed
    if request.method == 'POST' and 'delete-completed' in request.form:
        Checklist.delete_all_completed_items(user_id=current_user.id)
        return render_frame(template='_checklist_update.html', target='checklist-content', method='replace',
                            content=Checklist.get_completed_items(user_id=current_user.id))
    # delete all checklist
    if request.method == 'POST' and 'delete-checklist' in request.form:
        Checklist.delete_checklist(user_id=current_user.id)
        return render_frame(template='_checklist_update.html', target='checklist-content', method='replace',
                            content=Checklist.get_completed_items(user_id=current_user.id))

    return render_template('checklist.html', completed_items=completed_items)



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
    app.run(debug=False)
