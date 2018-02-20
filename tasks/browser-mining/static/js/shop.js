function buy(){
    fetch('/shop', {method: 'POST', credentials: 'include'})
    .then(resp=>{
        if (!resp.ok){
            throw new Error(resp.statusText);
        }
        return resp.json();
    }).then(resp=>{
        if (!resp['flag']){
            throw new Error(resp['error']);
        }
        else {
            $('.flag').html(resp['flag']).show();
            $('#balance').html(Number(resp['balance']));        
        }
    })
    .catch(error=>c0coc0('.shop-error', error));
}