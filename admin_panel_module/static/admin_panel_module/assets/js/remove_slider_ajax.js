function removeSlider(sliderId) {
    "Send request with get for url to remove slider with ajax and show the result with sweet alert"
    event.preventDefault();
    Swal.fire({
        title: "تایید حذف اسلایدر",
        text: "آیا میخواهید اسلایدر حذف شود؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "تایید",
        cancelButtonText: "لغو",
    }).then(firstSweetRe => {
        if (firstSweetRe.isConfirmed) {
            $.get("../slider/remove-slider/", {
                "id": sliderId,
            }).then(re => {
                if (re.status === "ok") {
                    Swal.fire({
                        title: "حذف اسلایدر",
                        text: "اسلایدر حذف شد",
                        icon: "success",
                        showCancelButton: false,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "خروج"
                    }).then(sweetRe => {
                        if (sweetRe.isConfirmed) {
                            location.href = "../slider/"
                        }
                    })

                } else {
                    Swal.fire({
                        title: "ارر",
                        text: "اسلایدر حذف نشد\n خطایی رخ داد",
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