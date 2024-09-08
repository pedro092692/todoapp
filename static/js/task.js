function send_search_form(){

    try{
        form = document.getElementById('search-form');
        input = document.getElementById('search-input');
        input.addEventListener('keyup', function(){
            form.requestSubmit();
        })
    }catch{
        //pass
    }
}

function show_detail(task){
    const panel = document.getElementById('more-info');
    let form = task.children[1];
    form.requestSubmit();
    panel.style.display = 'flex';

}

function close_panel(){
    const panel_section = document.getElementById('more-info');
    const more_info = document.getElementById('more-info-js');
    for(let child of panel_section.children){
        child.style.display = 'none';

    }
    panel_section.style.display = 'none';
    more_info.remove();
}

function completed_task(checkbox){
    let id = checkbox.getAttribute('id');
    let form = document.getElementById('check-' + id);
    form.requestSubmit();
}

function show_completed_task(){
    try{
        const completed_container = document.getElementById('completed');
        const arrow = completed_container.children[1];
        const completed_list = document.getElementById('completed-list');
        let state = false;
        completed_container.addEventListener('click', ()=>{
            if(!state){
                show(degrees='90', display='flex');
                state = true;
            }else{
                show(degrees='0', display='none');
                state = false;
            }
        })

        function show(degrees, display){
            arrow.style.transform = 'rotate('+degrees+'deg)';
            completed_list.style.display = display;
        }
    }catch{
//        pass
    }
}


send_search_form();
show_completed_task();




