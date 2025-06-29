function isActiveChanged(sliderId) {
    let checkBox = document.getElementById("is_active_button_slider_component");
    let isChecked = checkBox.checked ? true : false;

    if (isChecked) {
        console.log("Checked!")
        $.get("./set-slider-enable/", {
            "id": sliderId,
        })
    } else {
        console.log("unchecked!")
        $.get("./set-slider-disable/", {
            "id": sliderId,
        })
    }
}