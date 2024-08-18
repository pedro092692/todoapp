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

show_step_form();