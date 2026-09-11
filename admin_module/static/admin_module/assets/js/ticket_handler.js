function SetTickerClose(ticket_id) {
    $.get("set-ticket-close/" + ticket_id + "/").then(re => {
        Swal.fire({
            title: re.title,
            text: re.msg,
            icon: re.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: 'بستن',
        }).then(finally_result => {
            location.reload();
        })
    })
}