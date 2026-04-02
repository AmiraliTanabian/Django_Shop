// get csrf_token
// var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var btn = document.getElementById("price_filter_btn");
btn.addEventListener('click', function () {
    // sl2 : price filter input
    value = document.getElementById("sl2").getAttribute('data-slider-value');
    $.get("/products/price-fiter", {
        "value": value,
    })
})