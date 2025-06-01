$('#date-picker').persianDatepicker({
    format: 'YYYY/MM/DD',
    calendar: {
        persian: {
            locale: 'fa'
        }
    }
});


function removeMsgAdmin(msgId) {
    evenet.preventDefault();
    Swal.fire({
        title: 'تایید حذف',
        text: 'آیا شما از حذف پیام مطمنئنید؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "حذف"
    }).then((result) => {
        confirmButtonText: "حذف"
        if (result.isConfirmed) {
            $.get("../remove-msg/", {
                "msg_id": msgId,
            }).then(re => {
                console.log(re)
            })
        }
    });
}