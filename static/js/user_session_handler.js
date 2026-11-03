function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function set_session_logout(session_key) {
    const data = new URLSearchParams({
        session_key: session_key
    });

    fetch('/profile/logout-session/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    }).then(response => response.json()).then(re => {
        Swal.fire({
            title: re.title,
            text: re.msg,
            icon: re.icon,
            confirmButtonText: "اوکی",
        }).then(sweet_alert_re => location.reload());
    })
}

