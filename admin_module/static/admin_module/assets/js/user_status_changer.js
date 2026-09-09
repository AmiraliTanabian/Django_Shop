const user_status_label = document.getElementById("user_status_label");
const user_status_btn = document.getElementById("user_status_btn");

function setUserActive(id) {
    $.get("set-user-enable/" + id + "/").then(re => {
        if (re.success) {
            user_status_label.innerText = "فعال";
            user_status_label.className = "label label-green";
            user_status_btn.innerText = "کاربر رو غیرفعال کن";
            user_status_btn.className = "btn btn-danger btn-sm";
            user_status_btn.onclick = () => setUserDisable(id);

        }
    })
}

function setUserDisable(id) {
    $.get("set-user-diable/" + id + "/").then(re => {
        if (re.success) {
            user_status_label.innerText = "غیرفعال";
            user_status_label.className = "label label-red";
            user_status_btn.innerText = "کاربر رو فعال کن";
            user_status_btn.className = "btn btn-success btn-sm";
            user_status_btn.onclick = () => setUserActive(id);
        }
    })
}