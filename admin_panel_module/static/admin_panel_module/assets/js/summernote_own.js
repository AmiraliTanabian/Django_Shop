$(document).ready(function () {
    $('#summernote').summernote();

    $('#myForm').on('submit', function () {
        var content = $('#summernote').summernote('code');
        $('#article_content').val(content);
    });
});