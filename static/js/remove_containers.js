// чистка элементов контейнеров
function clear(){
    let search_inp = document.querySelector('#search_inp');
    if (search_inp) search_inp.remove();
    let find_link = document.querySelector('#find_link');
    if (find_link) find_link.remove()
    let drop_field = document.querySelector('#drop_field');
    if (drop_field) drop_field.remove();
    
    let scriptElementDrop = document.querySelector('#script_drop');
    if (scriptElementDrop)scriptElementDrop.remove();
    let scriptElement = document.querySelector('#script_noise');
    if (scriptElement)scriptElement.remove();

    let search_input = document.querySelector('#search_input');
    if (search_input) search_input.remove();
    let search_submit_btn = document.querySelector('#search_submit_btn');
    if (search_submit_btn) search_submit_btn.remove();

}

