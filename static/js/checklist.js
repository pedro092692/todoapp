function complete_checklist_item(){

    let completed_checkboxes = document.querySelectorAll('.completed-checkbox');

    if(completed_checkboxes){
        for(let checkbox of completed_checkboxes){
            checkbox.addEventListener('click', ()=>{
                let form = checkbox.parentNode;
                form.requestSubmit();
            })
        }
    }
}

complete_checklist_item();