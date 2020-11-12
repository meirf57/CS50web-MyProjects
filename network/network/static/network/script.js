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
        const text = button.textContent;
        const str = `like-${id}`;
        const like_id = str.replace('like-', '');
        if (text==whiteheart){
            like(like_id, "positive");
            button.textContent=redheart;
        } else {
            like(like_id, "negative");
            button.textContent=whiteheart;
        }
    }
})

function like(id, num) {
    fetch("/like/", {
        method : "PUT",
        body : JSON.stringify({
        id : id,
        num : num
    })
    })
    .then((res) => res.json())
    .then((res) => { 
        if (res.status == 201) {
            console.log(`like_count = ${res.like_count}`);
            console.log(`like_id = ${res.like_id}`);
            changenum(id, res.like_id, res.like_count);            
        }
    })
    .catch(function (res) {
        alert(res.message);
    });
}

function changenum(idbtn, idtxt, num) {
    var element = document.getElementById(idtxt);
    element.parentNode.removeChild(element);
    var item = document.createElement("i");
    item.setAttribute("id", idtxt);
    item.innerHTML = num;
    var div = document.getElementById(idbtn);
    insertAfter(div, item);
}

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }
