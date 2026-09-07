function RemoveProduct(id) {
    Swal.fire({
        title: 'حدف محصول',
        text: "آیا مطمنی که محصول با شناسه " + id + " حذف شود؟",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "حذف",
        cancelButtonText: "لغو"

    }).then((re) => {
        if (re.isConfirmed) {
            $.get("./remove-product/" + id + "/", {}).then(re => {
                Swal.fire({
                    title: re.title,
                    text: re.msg,
                    icon: re.icon,
                    showCancelButton: false,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: 'بستن',
                })
            }).then(finally_result => location.href = "./")


        }
    })
}