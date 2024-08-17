//function send_form(){
//    form = document.getElementById('form');
//    input = document.getElementById('input');
//    input.addEventListener('keyup', function(){
//        form.requestSubmit();
//    })
//}

//send_form();

function show_add_form(){
    const add_button = document.getElementById('add-button');
    const form = document.getElementById('add-form');
    add_button.addEventListener('click', ()=>{
       add_button.style.display = 'none';
       form.style.display = 'block';
       form.children[0].value = '';
       form.children[0].focus();
    })

    form.addEventListener('submit', ()=>{
        add_button.style.display = 'block';
        form.style.display = 'none';
    })
}

show_add_form();