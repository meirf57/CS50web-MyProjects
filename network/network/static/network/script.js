document.addEventListener('DOMContentLoaded', function() {
    const whiteheart = '🤍'; 
    const redheart = '❤';

    var buttons = document.getElementsByTagName("button");
    var buttonsCount = buttons.length;
    for (var i = 0; i <= buttonsCount; i += 1) {
        buttons[i].onclick = function(e) {
            toggle(this.id);
            // post id = "like- {number}" so minus first 5 char is id
        };
    }

    function toggle(id){
        const button = document.querySelector(`#${id}`);
        const text = button.textContent;
        if (text==whiteheart){
            button.textContent=redheart;
        } else {
            button.textContent=whiteheart;
        }
    }
})

