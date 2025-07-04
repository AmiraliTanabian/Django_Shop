function setProductCommentApproved(commentId){
    $.get("./set-approved/", {
        "id":commentId,
    }).then(re => {
        if (re.status === "ok"){
        Swal.fire({
            text: "کامنت تایید شد.",
            icon: "success",
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: "بستن",
    }).then(sweetAlertResult => {
        location.reload();
        })
        }
        else {
        Swal.fire({
            text: "کامنت مورد نظر تایید نشد!",
            icon: "error",
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: "بستن",
    }).then(sweetAlertResult => {
        location.reload();
        })
        }
    })
}

function setProductCommentRejected(commentId){
    $.get("./set-rejected/", {
        "id":commentId,
    }).then(re => {
        if (re.status === "ok"){
        Swal.fire({
            text: "کامنت رد شد.",
            icon: "success",
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: "بستن",
    }).then(sweetAlertResult => {
        location.reload();
        })
        }
        else {
        Swal.fire({
            text: "کامنت مورد نظر رد نشد!",
            icon: "error",
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: "بستن",
    }).then(sweetAlertResult => {
        location.reload();
        })
        }
    })
}