function show_menu(){
    let opened = false;
    let div = document.createElement('div');
    const menu = document.getElementById('menu');
    const nav = document.querySelector('nav');
    const more_info = document.getElementById('more-info');
    const main = document.getElementById('main');
    if(menu){
        menu.addEventListener('click', ()=>{
            div.classList.add('bg');
            main.prepend(div);
            if(more_info && more_info.style.display == 'flex'){
                more_info.style.display = 'none';
            }
            nav.style.display = 'flex';
            opened = true;

            addEventListener('click', (event)=>{
            if(!event.composedPath().includes(nav) && !event.composedPath().includes(menu) && opened){
                nav.style.removeProperty('display');
                div.remove();
            }
        })


        })
    }
}

function show_add_form(form_id, trigger){
    try{
        const add_button = document.getElementById(trigger);
        const form = document.getElementById(form_id);
        if(add_button){
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

    }catch{
        //pass
    }
}

if(window.location['pathname'] == '/'){
    show_add_form('add-form', 'add-button');
}else if (window.location['pathname'] == '/checklist'){
    show_add_form('add-item-check', 'add-item');
}

show_menu();