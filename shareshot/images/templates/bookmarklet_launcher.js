(
    function(){
    if   (window.mybookmarklet!==undefined){
            mybookmarklet();
        }
    else{
        document.body.appendChild(document.createElement('script')).src='https://4171-103-204-169-253.ngrok.io/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999)
    }
}
)();