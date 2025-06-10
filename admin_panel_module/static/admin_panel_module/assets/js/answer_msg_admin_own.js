function toggleModal(show) {
    const popUp = document.getElementById('popup');
    popUp.style.display = show ? 'flex' : 'none';
    popUp.className = "fixed inset-0 bg-black bg-opacity-50 items-center justify-center z-50";
}

function submitReply() {
    const text = document.getElementById('replyText').value.trim();
    if (text) {
        alert("پاسخ ثبت شد:\n" + text);
        toggleModal(false);
        document.getElementById('replyText').value = '';
    } else {
        alert("لطفاً پاسخ را وارد کنید!");
    }
}