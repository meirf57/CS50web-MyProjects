function add_form() {
    var element = document.querySelector('#item-form');
    element.setAttribute("style", "display: block;");
    var plus = document.querySelector('#add-form');
    plus.setAttribute("style", "display: none;");
}


function add_comment(id) {
    // get plus id 
    var title = document.getElementById(`title-${id}`);

    // create form element to edit text
    var form = document.createElement("div");
    form.setAttribute("id", `form-${id}`);
    form.innerHTML = `<form onsubmit="return false"><textarea class="form-control" id="comment-${id}"></textarea>
    <input type="submit" onclick="new_comment(${id});" class="btn btn-primary" value="Post."/></form>`;

    insertAfter(title, form);
}


function new_comment(id) {
    // Get value of form
    var text = document.getElementById(`comment-${id}`).value;
    var id = id;

    // Had to separate in to 2
    add_txt(id, text);
}


function add_txt(id, txt){
    fetch('/addPost/', {
        method: "PUT",
        body: JSON.stringify({
        id : id,
        txt: txt
        })
        })
    .then(response => response.json())
    .then(res => {
        if (res.status == 201) {
            // update post
            upPost(res.post_id, res.text);
            console.log(res.post_id)
            console.log(res.text)
            return false;          
        }
    })
    .catch(function (res) {
        alert(res.message);
    });
}


function upPost(id, text){
   
    // get form element
    var form = document.getElementById(`form-${id}`);
    form.parentNode.removeChild(form);

    // remove old comments
    var oldul = document.getElementById(`item-list-${id}`);
    oldul.parentNode.removeChild(oldul);

    // get title placement
    var title = document.getElementById(`title-${id}`);
    // create p element to place new comment
    var ilist = document.createElement("div");
    ilist.setAttribute("id", `item-list-${id}`);
    ilist.setAttribute("style", "padding-left: 1em;");
    ilist.innerHTML = text;

    // insert new post
    insertAfter(title, ilist);
}


// insert new element after other element
function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }


// share func
function share(id){
    alert(`form working through js, list id: ${id}`)
}