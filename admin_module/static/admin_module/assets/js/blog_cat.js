function BlogCatRemove(id) {
    Swal.fire({
        title: 'حدف دسته بندی',
        text: 'آیا مطمن هستید که دسته بندی را حذف کنید؟',
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "حذف",
        cancelButtonText: "لغو"

    }).then((re) => {
        if (re.isConfirmed) {
            $.get("../remove-cat/" + id + "", {}).then(re => {
                console.log("My Result:")
                console.log(re)
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

function SetCatActive(id) {
    $.get('../set-active-cat/' + id + "/").then(re => Swal.fire({
        title: re.title,
        text: re.msg,
        icon: re.icon,
        showCancelButton: false,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: 'بستن',
    }))
    location.reload();
}

function SetCatDisable(id) {
    $.get('../set-disable-cat/' + id + "/").then(re => Swal.fire({
        title: re.title,
        text: re.msg,
        icon: re.icon,
        showCancelButton: false,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: 'بستن',
    }))
    location.reload();
}

function BlogTagRemove(id) {
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


function SetTagActive(id) {
    $.get('../set-active-tag/' + id + "/").then(re => Swal.fire({
        title: re.title,
        text: re.msg,
        icon: re.icon,
        showCancelButton: false,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: 'بستن',
    }))
    location.reload();
}

function SetTagDisable(id) {
    $.get('../set-disable-tag/' + id + "/").then(re => Swal.fire({
        title: re.title,
        text: re.msg,
        icon: re.icon,
        showCancelButton: false,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: 'بستن',
    }))
    location.reload();
}