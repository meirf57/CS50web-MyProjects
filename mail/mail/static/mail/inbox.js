document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // When form is submited 'send' email
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#message').style.display = 'none';
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

  // Remove message block if switched to other page
  if (mailbox != 'inbox') {
    document.querySelector('#message').style.display = 'none';
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch this 'mailbox' data to load on page 
  console.log(mailbox);
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    // email row will set each email in it's row
    emails.forEach(email => email_row(email));
  });
}


function email_row(email) {

  // card for each email
  const item = document.createElement('div');
  item.setAttribute('class', 'card');
  item.setAttribute('id', `row-${email.id}`);

  // color grey if read
  var color;
  if (!email.read) {
    color = 'white';
  } else {
    color = '#d3d3d3';
  }
  // not sure why this yes and in innerHTML no
  item.style.backgroundColor = color;

  // set cards inner html with appropiate data
  item.innerHTML = `<div class="card-body" id="item-${email.id} style="color:${color};">
  <h5>Subject: ${email.subject}</h5><br>
  From: ${email.sender}  |  To: ${email.recipients}<br>
  ${email.body.slice(0,100)}</div>
  <div class="card-footer">
  <small class="text-muted">Time: ${email.timestamp}</small>
  </div>`;

  // If clicked show email
  item.addEventListener('click', () => show_email(email.id));

  // Append to viewBlock
  document.querySelector('#emails-view').appendChild(item);
}


function show_email(id) {

  // Get this email data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    // Clear viewBlock 
    document.querySelector('#emails-view').innerHTML = '';

    // Create view of email
    var item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `<div class="card-body" style="white-space:pre-wrap">
    <h5>Subject: ${email.subject}</h5>
    Sender: ${email.sender}
    Recipients : ${email.recipients}
    <p>${email.body}</p>
    </div>`;

    // Card footer for time stamp
    var footer = document.createElement('div');
    footer.innerHTML = `<div class="card-footer">
    <small class="text-muted">Time: ${email.timestamp}</small>
    </div>`
    document.querySelector('#emails-view').appendChild(item);

    // Mark as read
    email_read(email.id);
    if (!email.read) {
      email_read(email.id);
    }

    // Button to archive email
    var archive = document.createElement("button");
    archive.className = "btn btn-outline-success";
    archive.setAttribute('id', 'archive-btn');
    archive.addEventListener('click', () => {
      email_archive(id, email.archived), load_mailbox('inbox');

      // Set inner button text
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

    // Create reply button
    var reply = document.createElement("button");
    reply.className = "btn btn-outline-info";
    reply.setAttribute('id', 'reply-btn');
    reply.innerText = "Reply";
    reply.addEventListener('click', () => {
      email_reply(email.sender,email.subject,email.body,email.timestamp);
    });

    // Append buttons and footer
    item.append(reply, archive, footer);
  });
}

function email_read(id) {

  // Set email as read
  fetch(`/emails/${id}`, {
    method: "PUT",
    body : JSON.stringify({
      read : true
    })
  });
}

function email_archive(id, state) {

  // Redirect to inbox
  load_mailbox('inbox');

  // Success message
  document.querySelector('#message').style.display = 'block';
  document.querySelector('#message').innerHTML = `<div class="alert alert-success" role="alert">Email Archive Modified!</div>`;

  // Set as archived
  fetch(`/emails/${id}`, {
    method : "PUT",
    body : JSON.stringify({
      archived : !state
    })
  });
}

function email_reply(sender, subject, body, timestamp) {

  // Get compose mail page
  compose_email();

  // Set prefill as in reply
  subject = `${subject.substring(0, 4)==='Re: ' ? '' : 'Re: '}${subject}`;
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = subject;
  pre_fill = `On: ${timestamp}\n${sender} wrote:  ${body}\n `;
  document.querySelector('#compose-body').value = pre_fill;
}


function send_email() {

  // Get values of form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Had to separate in to 2 to redirect to 'sent'
  send_email2(recipients, subject, body);
  return false;
}

function send_email2(recipients, subject, body) {

  // Part 2, POST form as new email
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

    // Redirect to 'sent'
    load_mailbox('sent');

    // Success message
    document.querySelector('#message').style.display = 'block';
    document.querySelector('#message').innerHTML = `<div class="alert alert-success" role="alert">Email Sent!</div>`;
  });
}