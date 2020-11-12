document.addEventListener('DOMContentLoaded', function() {
    // variables for hearts
    const whiteheart = '🤍'; 
    const redheart = '❤';

    // getting button data
    var buttons = document.getElementsByTagName("button");
    var buttonsCount = buttons.length;
    for (var i = 0; i <= buttonsCount; i += 1) {
        buttons[i].onclick = function(e) {
            toggle(this.id);
        };
    }

    // toggle between hearts, and call like function to change likes
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


// add or remove likes
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
            // update number of likes displayed
            changenum(id, res.like_id, res.like_count);            
        }
    })
    .catch(function (res) {
        alert(res.message);
    });
}


// remove old- make and add new like amount after button 
function changenum(idbtn, idtxt, num) {
    var element = document.getElementById(idtxt);
    element.parentNode.removeChild(element);
    var item = document.createElement("i");
    item.setAttribute("id", idtxt);
    item.innerHTML = num;
    var div = document.getElementById(idbtn);
    insertAfter(div, item);
}


// insert new element after other element
function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }
