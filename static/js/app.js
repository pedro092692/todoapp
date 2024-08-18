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



function show_add_form(){
    const add_button = document.getElementById('add-button');
    const form = document.getElementById('add-form');


    addEventListener('click', (event)=>{
        if(!event.target.contains(add_button) && !event.target.contains(form.children[0]) && form.children[0].value == ''){
            hide_form();
        }
    })

    add_button.addEventListener('click', ()=>{
       add_button.style.display = 'none';
       form.style.display = 'flex';
       form.children[0].value = '';
       form.children[0].focus();
    })

    form.addEventListener('submit', (event)=>{
        form.children[1].value = form.children[0].value;
        form.children[0].value = '';

        console.log('value of task', form.children[1].value)
    })



    function hide_form(){
        add_button.style.display = 'block';
        form.style.display = 'none';
    }
}

function show_detail(task){
    const panel = document.getElementById('more-info');
    let form = task.children[2];
    form.requestSubmit();
    panel.style.display = 'flex';

}

function close_panel(){
    const panel_section = document.getElementById('more-info');
    panel_section.style.display = 'none';

}

show_add_form();
send_search_form();

