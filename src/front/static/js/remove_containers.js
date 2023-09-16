function clear(){
    const search_inp = document.querySelector('#search_inp')
    const find_link = document.querySelector('#find_link')
    const drop_field = document.querySelector('#drop_field')
    const search_submit_btn = document.querySelector('#search_submit_btn')
    // const canva = document.querySelector('#noisy-canvas')

   

    if (search_inp) search_inp.remove() ;
    if (find_link) find_link.remove() ;
    if (drop_field) drop_field.remove() ;
    if (search_submit_btn) search_submit_btn.remove() ;
    // if (canva) canva.remove() ;

    const scriptElementDrop = document.querySelector('#script_drop');
    if (scriptElementDrop)scriptElementDrop.remove();
    const scriptElement = document.querySelector('#script_noise');
    if (scriptElement)scriptElement.remove();
}

