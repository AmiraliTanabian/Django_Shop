function RemoveBrand(id) {
    Swal.fire({
        title: 'حدف برند',
        text: 'آیا مطمن هستید که برند را حذف کنید؟',
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "حذف",
        cancelButtonText: "لغو"

    }).then((re) => {
        if (re.isConfirmed) {
            $.get("../remove-brand/" + id, {}).then(re => {
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


function SetProductBrandActive(id) {
    $.get('../set-active-brand/' + id + "/").then(
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

function SetProductBrandDisable(id) {
    $.get('../set-disable-brand/' + id + "/").then(
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