function removeBanner(sliderId) {
    "Send request with get for url to remove banner with ajax and show the result with sweet alert"
    event.preventDefault();
    Swal.fire({
        title: "تایید حذف تبلیغ",
        text: "آیا میخواهید تبلیغ ( بنر ) حذف شود؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "تایید",
        cancelButtonText: "لغو",
    }).then(firstSweetRe => {
        if (firstSweetRe.isConfirmed) {
            $.get("../remove-banner/", {
                "id": sliderId,
            }).then(re => {
                if (re.status === "ok") {
                    Swal.fire({
                        title: "حذف تبلیغ",
                        text: "تبلیغ حذف شد",
                        icon: "success",
                        showCancelButton: false,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "خروج"
                    }).then(sweetRe => {
                        if (sweetRe.isConfirmed) {
                            location.href = "./.."
                        }
                    })

                } else {
                    Swal.fire({
                        title: "ارر",
                        text: "تبلیغ حذف نشد\n خطایی رخ داد",
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