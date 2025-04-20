function addToOrder(productId) {
    event.preventDefault();
    let productCount = $("#product_count").val();
    $.get("../order/add-to-order", {
        count: productCount,
        product_id: productId,
    }).then(re => {
        console.log(re);
        Swal.fire({
            title: re.title,
            text: re.text,
            icon: re.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "ورود به حساب"
        }).then((result) => {
            confirmButtonText: "ورود به حساب"
            if (result.isConfirmed && re.status === "not_auth") {
                location.href = "../../account/login"
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