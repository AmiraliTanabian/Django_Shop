function removeProductOnProductList(sliderId) {
    event.preventDefault();
    Swal.fire({
        title: "تایید حذف محصول",
        text: "آیا میخواهید محصول حذف شود؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "تایید",
        cancelButtonText: "لغو",
    }).then(firstSweetRe => {
        if (firstSweetRe.isConfirmed) {
            $.get("./remove-product/", {
                "id": sliderId,
            }).then(re => {
                if (re.status === "ok") {
                    Swal.fire({
                        title: "حذف محصول",
                        text: "محصول حذف شد",
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
                        text: "محصول حذف نشد\n خطایی رخ داد",
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

function changeProductCount(productId) {
    let count = document.getElementById("quantity" + productId).value;
    $.get("./change-count/", {
        "id": productId,
        "count": count,
    }).then(re => {
        console.log(re)
    })
}
