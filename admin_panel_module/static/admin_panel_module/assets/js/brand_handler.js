function brandHandlerOnBrandList(brandId) {
    let brand_is_active_element = document.getElementById("brand_is_active");
    let is_checked;
    if (brand_is_active_element.checked) {
        $.get('./set-brand-enable/', {
            "id": brandId,
        }).then(re => {
            console.log(re)
        })
    } else {
        $.get('./set-brand-disable/', {
            "id": brandId,
        }).then(re => {
            console.log(re)
        })
    }

}

function removeBrandOnBrandList(brandId) {
    event.preventDefault();
    Swal.fire({
        title: "تایید حذف برند",
        text: "آیا میخواهید برند حذف شود؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "تایید",
        cancelButtonText: "لغو",
    }).then(firstSweetRe => {
        if (firstSweetRe.isConfirmed) {
            $.get("./remove-brand/", {
                "id": brandId,
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
