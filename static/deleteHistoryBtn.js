const delHistoryBtn = document.getElementById('delete-history-btn');

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

if (delHistoryBtn !== null) {

    delHistoryBtn.onclick = function () {
        const xhr = new XMLHttpRequest();
        const method = 'POST';
        const url = "/history-all-delete";
        const responseType = "json";
        const csrftoken = getCookie('csrftoken');

        xhr.open(method, url)
        xhr.setRequestHeader("Content-Type", "application/json")
        xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
        xhr.onload = function () {
            location.reload()
        }
        xhr.send();
        return
    }
}
