function addComment(articleId, site_url) {
    event.preventDefault();
    let commentText = $("#message").val()
    let parentId = $("#parentId").val()

    // $.get("http://localhost:8000/blog/add_comment/", {
    $.get(site_url + "blog/add_comment/", {
        comment_text: commentText,
        article_id: articleId,
        parent_id: parentId
    }).then(re => {
        location.reload()
    });

}

function setParentId(parentId) {
    $("#parentId").val(parentId)
    document.getElementById("comment-box").scrollIntoView({behavior: "smooth"})

}
