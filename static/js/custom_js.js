setTimeout(function () {
    var errorBox = document.getElementById("error-message");
    if (errorBox) {
        errorBox.style.opacity = "0";
        setTimeout(() => errorBox.remove(), 500);
    }
}, 3000);


function bigImage(imageSrc) {
    event.preventDefault();
    console.log("Hi!")
    let mainImage = document.getElementById("main-image")
    let mainImageBiggerButton = document.getElementById("main-image-bigger-link")
    mainImage.setAttribute("src", imageSrc)
    mainImageBiggerButton.setAttribute("href", imageSrc)

}