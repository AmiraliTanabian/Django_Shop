const answer_box = document.getElementById("answer_box");


function sendMsgAnswer(id) {
    $.get('./send-answer/', {
        "answer": answer_box.value,
        "id": id
    }).then(re => {
        Swal.fire({
            title: re.title,
            text: re.msg,
            icon: re.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "بستن"
        })
    })
}