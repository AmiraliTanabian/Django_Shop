const min_price = document.getElementById('min_price');
const max_price = document.getElementById('max_price');
const button = document.getElementById("button");
const price_filter = document.getElementById("sl2");

button.addEventListener('click', function () {
    console.log('i am here')
    let result = price_filter.value.split(',');
    min_price.value = result[0];
    max_price.value = result[1];
});

