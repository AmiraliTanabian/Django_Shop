setTimeout(function() {
    var errorBox = document.getElementById("error-message");
    if (errorBox) {
        errorBox.style.opacity = "0";
        setTimeout(() => errorBox.remove(), 500);
    }
}, 3000);

function addComment(articleId, url){
    console.log("Script loaded!")
    let commentText = $("#message").val()
    let parentId = $("#parentId").val()

    $.get(url, {
        comment_text : commentText,
        article_id : articleId,
        parent_id : parentId
    }).then(re => {
        console.log(re);
        location.reload();
});


}

function setParentId(parentId){
    $("#parentId").val(parentId)
}