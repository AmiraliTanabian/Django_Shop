function removeProductGallery(id) {
    $.get("./remove-gallery/" + id + "/").then(re => {
        if (re.status === "ok") {
            location.reload()
        }
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function galleryUploader(input, product_id) {
    const file = input.files[0];

    const formData = new FormData();
    formData.append("file", file);
    formData.append("product_id", product_id)
    fetch("./add-product-gallery/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload()
            }
        })
}