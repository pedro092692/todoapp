function complete_checklist_item(query){

    let completed_checkboxes = document.querySelectorAll(`.${query}`);

    if(completed_checkboxes){
        for(let checkbox of completed_checkboxes){
            checkbox.addEventListener('click', ()=>{
                let form = checkbox.parentNode;
                form.requestSubmit();
            })
        }
    }
}

function delete_checklist(form_idm, trigger, title){
    const delete_container = document.getElementById('delete-container');
    const cancel_button = document.getElementById('cancel-button');
    const confirm_button = document.getElementById('delete-button');
    let delete_title = document.getElementById('delete-title');

    const delete_button = document.getElementById(trigger);
    const form = select_form(form_id);

    if(form){
        if(delete_button){
            delete_button.addEventListener('click', (event)=>{
               event.preventDefault();
               delete_title.innerText = title;
               delete_container.style.display = 'flex';

            })
         }

        cancel_button.addEventListener('click', (event)=>{
            event.preventDefault();
            delete_container.style.display = 'none';
        })

        confirm_button.addEventListener('click', (event)=>{
            event.preventDefault();
            form.requestSubmit();
            delete_container.style.display = 'none';
        })
    }

}

function select_form(form_id){
    let form = document.getElementById(form_id);
    return form
}

delete_checklist(form_id='delete-all-completed-form', trigger='delete-checklist', title='Delete All Completed Items?');
delete_checklist(form_id='delete-checklist-form', trigger='checklist-all', title='Delete All Item?');
complete_checklist_item('completed-checkbox');
complete_checklist_item('uncompleted-checkbox');
