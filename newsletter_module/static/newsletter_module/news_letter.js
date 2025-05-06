function AddToNewsLetter() {
    console.log("salam")
    let email = $("#news_letter_email").val();
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