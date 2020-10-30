document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  console.log(mailbox);
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => email_row(email));
  });
}


function email_row(email) {
  const item = document.createElement('div');
  item.setAttribute('class', 'container');
  item.setAttribute('id', `row-${email.id}`);
  var color;
  if (!email.read) {
    color = 'white';
  } else {
    color = '#E8E8E8';
  }
  item.style.backgroundColor = color;
  item.innerHTML = `<div class="card-body" id="item-${email.id}">
  Subject: ${email.subject} | Recipients: ${email.recipients} | Time: ${email.timestamp}
  <br>
  ${email.body.slice(0,100)}</div><br>`;
  item.addEventListener('click', () => show_email(email.id));
  document.querySelector('#emails-view').appendChild(item);
}


function show_email(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    document.querySelector('#emails-view').innerHTML = '';
    var item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `<div class="card-body" style="white-space:pre-wrap">
    Sender: ${email.sender}
    Recipients : ${email.recipients}
    Subject : ${email.subject}
    Time : ${email.timestamp}
    ${email.body}
    </div>`;
    document.querySelector('#emails-view').appendChild(item);
    email_read(email.id);
    if (!email.read) {
      email_read(email.id);
    }

    var archive = document.createElement("button");
    archive.className = "btn btn-outline-success";
    archive.setAttribute('id', 'archive-btn');
    archive.addEventListener('click', () => {
      email_archive(id, email.archived);
      if (archive.innerText != "Archive") {
        archive.innerText = "Archive";
      } else {
        archive.innerText = "Unarchive";
      }
    });
    if (!email.archived) {
      archive.textContent = "Archive"
    } else {
      archive.textContent = "Unarchive";
    }

    var reply = document.createElement("button");
    reply.className = "btn btn-outline-info";
    reply.setAttribute('id', 'reply-btn');
    reply.innerText = "Reply";
    reply.addEventListener('click', () => {
      email_reply(email.sender,email.subject,email.body,email.timestamp);
    });
    item.append(reply, archive);
  });
}

function email_read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body : JSON.stringify({
      read : true
    })
  });
}

function email_archive(id, state) {
  fetch(`/emails/${id}`, {
    method : "PUT",
    body : JSON.stringify({
      archived : !state
    })
  });
}

function email_reply(sender, subject, body, timestamp) {
  // get compose mail page and prefill as reply
  compose_email();
  subject = `${subject.substring(0, 4)==='Re: ' ? '' : 'Re: '}${subject}`;
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = subject;
  pre_fill = `${sender} wrote: \n ${body} \n On: ${timestamp} \n`;
  document.querySelector('#compose-body').value = pre_fill;
}


function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  send_email2(recipients, subject, body)
  return false;
}

function send_email2(recipients, subject, body) {
  fetch('/emails', {
    method: "POST",
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  });
}