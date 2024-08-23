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


    console.log(container);
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

edit_task();
show_step_form();