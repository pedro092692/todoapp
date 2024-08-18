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

    })



    function hide_form(){
        add_button.style.display = 'block';
        form.style.display = 'none';
    }
}

show_add_form();
send_search_form();