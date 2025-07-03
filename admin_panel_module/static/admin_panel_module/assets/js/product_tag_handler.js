function productTagIsActiveHandler(sliderId) {
    let checkBox = document.getElementById("product_tag_is_active");
    let isChecked = checkBox.checked ? true : false;

    if (isChecked) {
        $.get("./set-product-tag-enable/", {
            "id": sliderId,
        })
    } else {
        $.get("./set-product-tag-disable/", {
            "id": sliderId,
        })
    }
}


function removeProductTagOnList(productTagId) {
    event.preventDefault();
    Swal.fire({
        title: "تایید حذف تگ",
        text: "آیا میخواهید تگ حذف شود؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "تایید",
        cancelButtonText: "لغو",
    }).then(firstSweetRe => {
        if (firstSweetRe.isConfirmed) {
            $.get("./remove/", {
                "id": productTagId,
            }).then(re => {
                if (re.status === "ok") {
                    Swal.fire({
                        title: "حذف تگ",
                        text: "تگ حذف شد",
                        icon: "success",
                        showCancelButton: false,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "خروج"
                    }).then(sweetRe => {
                        if (sweetRe.isConfirmed) {
                            location.reload();
                        }
                    })

                } else {
                    Swal.fire({
                        title: "ارر",
                        text: "تگ حذف نشد\n خطایی رخ داد",
                        icon: "error",
                        showCancelButton: false,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "خروج"
                    })
                }
            })
        }
    })
}

function removeProductTagOnEditPage(productTagId) {
    event.preventDefault();
    Swal.fire({
        title: "تایید حذف تگ",
        text: "آیا میخواهید تگ حذف شود؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "تایید",
        cancelButtonText: "لغو",
    }).then(firstSweetRe => {
        if (firstSweetRe.isConfirmed) {
            $.get("./remove/", {
                "id": productTagId,
            }).then(re => {
                if (re.status === "ok") {
                    Swal.fire({
                        title: "حذف تگ",
                        text: "تگ حذف شد",
                        icon: "success",
                        showCancelButton: false,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "خروج"
                    }).then(sweetRe => {
                        if (sweetRe.isConfirmed) {
                            location.href = ".";
                        }
                    })

                } else {
                    Swal.fire({
                        title: "ارر",
                        text: "تگ حذف نشد\n خطایی رخ داد",
                        icon: "error",
                        showCancelButton: false,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "خروج"
                    })
                }
            })
        }
    })
}