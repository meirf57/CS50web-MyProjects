document.addEventListener('DOMContentLoaded', function() {
    const whiteheart = '🤍'; 
    const redheart = '❤';

    var buttons = document.getElementsByTagName("button");
    var buttonsCount = buttons.length;
    for (var i = 0; i <= buttonsCount; i += 1) {
        buttons[i].onclick = function(e) {
            toggle(this.id);
        };
    }
    
    function toggle(id){
        const button = document.querySelector(`#${id}`);
        const like = button.textContent;
        if (like==whiteheart){
            button.textContent=redheart;
        } else {
            button.textContent=whiteheart;
        }
    }
})


