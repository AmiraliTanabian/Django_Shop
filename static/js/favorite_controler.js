function AddToFavorite(productId){
    event.preventDefault();
    $.get("add-to-favorite", {
        "product_id" : productId,
    }).then(re => {
        console.log(re);
        location.reload();
    })
}


function AddToFavoriteOnHomePage(productId){
    event.preventDefault();
    $.get("products/add-to-favorite", {
        "product_id" : productId,
    }).then(re => {
        console.log(re);
        location.reload();
    })
}

function RemoveFavoriteOnHomePage(productId){
    event.preventDefault()
    $.get("products/remove-from-favorite", {
        "product_id":productId,
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


function RemoveFavoriteOnProfilePage(productId){
    event.preventDefault()
    $.get("../remove-from-favorite", {
        "product_id":productId,
    }).then(re => {
        console.log(re);
        location.reload();

    })
}