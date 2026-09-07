function ProductTagRemove(id) {
    Swal.fire({
        title: 'حدف تگ',
        text: 'آیا مطمن هستید که تگ را حذف کنید؟',
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "حذف",
        cancelButtonText: "لغو"

    }).then((re) => {
        if (re.isConfirmed) {
            $.get("../remove-tag/" + id, {}).then(re => {
                Swal.fire({
                    title: re.title,
                    text: re.msg,
                    icon: re.icon,
                    showCancelButton: false,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: 'بستن',
                })
            }).then(finally_result => location.reload())


        }
    })
}

function SetProductTagActive(id) {
    $.get('../set-active-tag/' + id + "/").then(
        re => {
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
        }
    )
}

function SetProductTagDisable(id) {
    $.get('../set-disable-tag/' + id + "/").then(
        re => {
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
        }
    )
}