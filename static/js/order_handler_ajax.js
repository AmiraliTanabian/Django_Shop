function addToOrder(productId) {
    let confirm;
    event.preventDefault();
    let productCount = $("#product_count").val();
    if (productCount === null) {
        productCount = 1
    }
    $.get("../order/add-to-order", {
        count: productCount,
        product_id: productId,
    }).then(re => {
        if (re.status === "not_auth") {
            confirm = "ورود به حساب کاربری";
        } else {
            confirm = "مشاهده سبد خرید";
        }
        Swal.fire({
            title: re.title,
            text: re.text,
            icon: re.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: confirm,

        }).then((result) => {
            if (result.isConfirmed && re.status === "not_auth") {
                location.href = "../../account/login"
                // confirmButtonText: "ورود به حساب"

            } else {
                location.href = "../order"
            }
        });
    })


}

function removeOrderProduct(productId) {
    event.preventDefault();
    $.get("../order/remove-from-order", {
        "product_id": Number(productId),
    }).then(re => {
        $("#container").html(re)
    })

}

function addCountProduct(productId) {
    event.preventDefault()
    $.get("../order/add-product-count", {
        "product_id": Number(productId),
    }).then(
        re => {
            $("#container").html(re);
        }
    )
}

function removeCountProduct(productId) {
    event.preventDefault()
    $.get("../order/remove-product-count", {
        "product_id": Number(productId),
    }).then(
        re => {
            $("#container").html(re);
        }
    )
}