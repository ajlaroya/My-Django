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
