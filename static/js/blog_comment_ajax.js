function addComment(articleId, site_url) {
    event.preventDefault();
    let commentText = $("#message").val()
    let parentId = $("#parentId").val()
    const comment_txt_box = document.getElementById("message");

    // $.get("http://localhost:8000/blog/add_comment/", {
    $.get(site_url + "blog/add_comment/", {
        comment_text: commentText,
        article_id: articleId,
        parent_id: parentId
    }).then(re => {
        document.body.insertAdjacentHTML("beforeend", re);
        comment_txt_box.value = "";
        // for hide result box
        setTimeout(function () {
            let errorBox = document.getElementById("error-message");
            if (errorBox) {
                errorBox.style.opacity = "0";
                setTimeout(() => errorBox.remove(), 500);
            }
        }, 3000);
        //
    });

}

function setParentId(parentId) {
    $("#parentId").val(parentId)
    document.getElementById("comment-box").scrollIntoView({behavior: "smooth"})

}
