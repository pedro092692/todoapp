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

show_menu();