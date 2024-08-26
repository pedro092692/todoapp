function show_step_form(){
    const step_form = document.getElementById('add-step-form');
    const add_step = document.getElementById('add-step');
    const container = document.getElementById('task-steps');

    addEventListener('click', (event)=>{
        if(!event.target.contains(add_step) && !event.target.contains(step_form.children[0]) && step_form.children[0].value == ''){
            hide_form();
        }
    })

     add_step.addEventListener('click', ()=>{
           add_step.style.display = 'none';
           step_form.style.display = 'flex';
           step_form.children[0].value = '';
           step_form.children[0].focus();
        })

        step_form.addEventListener('submit', (event)=>{
            container.classList.remove('d-none');
            step_form.children[1].value = step_form.children[0].value;
            step_form.children[0].value = '';
        })

        function hide_form(){
            add_step.style.display = 'block';
            step_form.style.display = 'none';
        }

}

function edit_task(){
    let task_title = document.querySelector('.more-info .task-detail .task-detail-item .list-item p');
    let form = document.getElementById('edit-form');
    let form_input = form[0];
    let changed_title = false;
    task_title.addEventListener('click', ()=>{
        task_title.setAttribute('contenteditable', 'True');
    })
    task_title.addEventListener('keyup', ()=>{
        form_input.value = task_title.innerText;
        changed_title = true;
    })

    document.addEventListener('click', (event)=>{
        if(!event.target.contains(task_title)){
            if(form.isConnected && changed_title){
                form.requestSubmit();
            }
        }
    })

}

function completed_subtask(checkbox){
    let form = checkbox.parentNode;
    form.requestSubmit();
}

function edit_subtask(){
    let subtask_container = document.querySelectorAll('.more-info .task-detail .task-steps .subtask-item .list-item p');
    let changed_title = false;
    let subtask = false;
    let form = false;

    for(let subtask_item of subtask_container){
        subtask_item.addEventListener('click', ()=>{
            subtask = subtask_item;
            subtask_item.setAttribute('contenteditable', 'true');
            change_subtask_title(subtask_item);
        });
    }

    function change_subtask_title(subtask){
        form = subtask.nextElementSibling;
        let form_input = form[1];
        subtask.addEventListener('keyup', ()=>{
            form_input.value = subtask.innerText;
            changed_title = true;
        })
    }

    document.addEventListener('click', ()=>{
        if(changed_title){
            if(form.isConnected && !event.target.contains(subtask)){
                form.requestSubmit();
            }
            subtask = false;
            form = false;
            changed_title = false;
            }
    })


}

function delete_task(){
    const trash_button = document.getElementById('delete-task');
    const delete_div = document.getElementById('delete-container');
    const cancel_button = document.getElementById('cancel-button');
    let task_title = document.getElementById('task-title').innerText;
    const task_name = document.getElementById('delete-task-title');
    if(task_title.length > 57){
        task_name.innerText = task_title.substring(0, 57) + '...';
    }else{
        task_name.innerText = task_title
    }

    trash_button.addEventListener('click', ()=>{
        delete_div.style.display = 'flex';

    })
    cancel_button.addEventListener('click', ()=>{
        delete_div.style.display = 'none';
    })

}

edit_task();
show_step_form();
edit_subtask();
delete_task();