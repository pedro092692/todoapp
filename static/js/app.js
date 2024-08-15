function send_form(){
    form = document.getElementById('form');
    input = document.getElementById('input');
    input.addEventListener('keyup', function(){
        form.requestSubmit();
    })
}

send_form();