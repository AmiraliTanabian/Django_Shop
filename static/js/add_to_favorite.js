function AddToFavorite(productId){
    event.preventDefault();
    $.get("add-to-favorite", {
        "product_id" : productId,
    }).then(re => {
        console.log(re);
    })
}