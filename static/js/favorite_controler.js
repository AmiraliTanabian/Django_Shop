function AddToFavorite(productId){
    event.preventDefault();
    $.get("add-to-favorite", {
        "product_id" : productId,
    }).then(re => {
        console.log(re);
        location.reload();
    })
}

function RemoveFavorite(productId){
    event.preventDefault()
    $.get("remove-from-favorite", {
        "product_id":productId,
    }).then(re => {
        console.log(re);
        location.reload();

    })
}