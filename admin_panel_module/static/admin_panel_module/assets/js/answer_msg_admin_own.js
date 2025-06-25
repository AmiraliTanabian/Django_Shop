function toggleModal(show) {
    const popUp = document.getElementById('popup-overlay');
    popUp.classList.toggle('hidden', !show);
}

function getCsrfToken() {
    const allCookies = document.cookie;
    let allCookiesSplit = allCookies.split(';')
    let csrfToken = allCookiesSplit.find(
        function (value) {
            if (value.includes("csrftoken")) {
                return true;
            }
            return false;

        })
    csrfToken = csrfToken.split("=")[1]
    return csrfToken;
}

function submitReply() {
    const text = document.getElementById('replyText').value.trim();
    const email = document.getElementById('user_email_ajax').innerHTML;
    if (text) {
        $.get('../contact-us/send-ans/', {
            "email": email,
            "text": text,
        }).then(re => {
            if (re.status === 'success') {
                Swal.fire({
                    title: 'پیام ارسال شد',
                    icon: 'success',
                    showCancelButton: false,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "اوکی",
                })

            }
        })
    } else {
        alert("لطفاً پاسخ را وارد کنید!");
    }
}