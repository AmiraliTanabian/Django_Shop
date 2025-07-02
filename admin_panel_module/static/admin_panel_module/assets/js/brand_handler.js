function brandHandlerOnBrandList(brandId) {
    let brand_is_active_element = document.getElementById("brand_is_active");
    let is_checked;
    if (brand_is_active_element.checked) {
        $.get('./set-brand-enable/', {
            "id": brandId,
        }).then(re => {
            console.log(re)
        })
    } else {
        $.get('./set-brand-disable/', {
            "id": brandId,
        }).then(re => {
            console.log(re)
        })
    }

}