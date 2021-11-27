function commentReplyToggle(parent_id) {
  const row = document.getElementById(parent_id);
  if (row.classList.contains('is-hidden')) {
    row.classList.remove('is-hidden');
  } else {
    row.classList.add('is-hidden');
  }
}

function showNotifications() {
  const container = document.getElementById('notification-container');
  if (container.classList.contains('is-hidden')) {
    container.classList.remove('is-hidden');
  } else {
    container.classList.add('is-hidden')
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Grabs CSRF token and sends AJAX request, redirects
function removeNotification(removeNotificationURL, redirectURL) {
  var xmlhttp = new XMLHttpRequest();
  const csrftoken = getCookie('csrftoken');
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == XMLHttpRequest.DONE) {
      if (xmlhttp.status == 200) {
        window.location.replace(redirectURL);
      }
      else {
        alert('There was an error.');
      }
    }
  };
  xmlhttp.open("DELETE", removeNotificationURL, true);
  xmlhttp.setRequestHeader("X-CSRFToken", csrftoken)
  xmlhttp.send();
}

function shareToggle(parent_id) {
  const row = document.getElementById(parent_id);
  if (row.classList.contains('is-hidden')) {
    row.classList.remove('is-hidden');
  } else {
    row.classList.add('is-hidden');
  }
}

// Dynamically finds tags and links them to explore page!
function formatTags() {
  var elements = document.getElementsByClassName('post-body');
  for (let i = 0; i < elements.length; i++) {
    let bodyText = elements[i].children[0].innerText;
    let words = bodyText.split(' ');
    for (let j = 0; j < words.length; j++) {
      if (words[j][0] === '#') {
        let replacedText = bodyText.replace(/\s\#(.*?)(\s|$)/g,
        ` <a href="/posts/explore?query=${words[j].substring(1)}">${words[j]}</a>`);
        elements[i].innerHTML = replacedText
      }
    }
  }
}

formatTags();

function dropdown() {
  document.querySelectorAll('.dropdown').forEach(item => {
      item.addEventListener('click', function(event) {
          event.stopPropagation();
          item.classList.toggle('is-active');
      });
  });
}

dropdown()
