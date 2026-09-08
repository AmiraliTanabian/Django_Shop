function removeProductGallery(product_id) {
    $.get("./remove-gallery/" + product_id + "/").then(re => {
        if (re.status === "ok") {
            const gallery_outer = document.getElementById("galleryGrid");
            gallery_outer.innerHTML = re.result;
        } else { // error
            Swal.fire({
                title: re.title,
                text: re.msg,
                icon: re.icon,
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "حذف",
                cancelButtonText: "لغو"

            })
        }
    })
}