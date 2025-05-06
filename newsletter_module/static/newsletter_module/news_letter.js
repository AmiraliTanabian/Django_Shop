function email_validation(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}


function AddToNewsLetter() {
    console.log("salam")
    let email = $("#news_letter_email").val();

    if (!email_validation(email)) {
        Swal.fire({
            title: 'ایمیل نامعتبر',
            text: 'ایمیل شما معتبر نمیباشد!',
            icon: 'error',
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
        })
    } else {
        $.get("news-letter/add", {
            "email": email,
        }).then(re => {
            console.log(re);
            Swal.fire({
                title: re.title,
                text: re.text,
                icon: re.icon,
                showCancelButton: false,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
            })
        })
    }


}