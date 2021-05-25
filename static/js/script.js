function criarListas(alvo,obj,lista){
    console.log(typeof(lista))
    o=document.getElementsByClassName(alvo);
    lista.forEach(element => {
        inst='<li class='+obj+'>'+element+'</li>';
        o.innerHTML+=inst;
        console.log(element);
    });


}

