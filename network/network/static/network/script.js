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
        var button = document.querySelector(`#${id}`);
        var text = button.textContent;
        if (text==whiteheart){
            like(id, "positive");
            button.textContent=redheart;
        } else {
            like(id, "negative");
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


// remove ol, make and add new like amount after button 
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


  function check_edit(id) {
    var link = document.querySelector(`#edit-${id}`);
    var lText = link.textContent;
    
    // if edit was clicked
    if (lText=="Edit") {

        // save text and remove element
        var element = document.getElementById(`post-${id}`);
        var post_text = element.innerHTML;
        element.parentNode.removeChild(element);

        // create new of same but no text
        var item = document.createElement("i");
        item.setAttribute("id", `post-${id}`);
        item.innerHTML = "";

        // set in same position as old one
        var div = document.getElementById(`creator-${id}`);
        insertAfter(div, item);

        // create form element to edit text
        var form = document.createElement("div");
        form.setAttribute("id", `form-${id}`);
        form.innerHTML = `<form onsubmit="return false"><textarea class="form-control" id="edit-${id}">${post_text}</textarea>
        <input type="submit" onclick="edit_txt(${id});" class="btn btn-primary"/></form>`;
        
        //hiding edit link
        link.textContent = '';

        // place where text used to be
        insertAfter(item, form);
    }
  }


  // get new text 
  function edit_txt(id) {
    // Get value of form
    const editT = document.getElementById(`edit-${id}`).value;
    const Tid = id;

    // Had to separate in to 2
    edit_txt2(Tid, editT);
    return false;
  }

  // Part 2, edit text
  function edit_txt2(Tid,editT) {  
    fetch('/editPost/', {
      method: "PUT",
      body: JSON.stringify({
        id : Tid,
        editT: editT
        })
      })
    .then(response => response.json())
    .then(res => {
        if (res.status == 201) {
            // update post
            upPost(res.post_id, res.text);
            return false;          
        }
    })
    .catch(function (res) {
        alert(res.message);
    });
    return false;
  }

  function upPost(id, text) {
      // save text and remove element
      var element = document.getElementById(`post-${id}`);
      element.parentNode.removeChild(element);
    
      // since form not acting regular have to remove
      var form = document.getElementById(`form-${id}`);
      form.parentNode.removeChild(form);

      // create new of same but no text
      var item = document.createElement("strong");
      item.setAttribute("id", `post-${id}`);
      item.innerHTML = text;

      // display edit link
      var link = document.querySelector(`#edit-${id}`);
      link.textContent = "Edit";

      // set in same position as old one
      var div = document.getElementById(`creator-${id}`);
      insertAfter(div, item);
      return false;
  }