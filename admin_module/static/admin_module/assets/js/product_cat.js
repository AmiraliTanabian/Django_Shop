function removeProductCategory(id) {
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

function setProductCategoryActive(id) {
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


function setProductCategoryDisable(id) {
    $.get('../set-disable-cat/' + id + "/").then(re => {
        Swal.fire({
            title: re.title,
            text: re.msg,
            icon: re.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: 'بستن',
        })
    })
    location.reload();
}
