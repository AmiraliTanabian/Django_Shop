function addToOrder(productId) {
    event.preventDefault();
    let productCount = $("#product_count").val();
    $.get("../order/add-to-order", {
        count: productCount,
        product_id: productId,
    }).then(re => {
        console.log(re);
    })
}