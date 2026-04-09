function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function previewFile(file, fileId = null) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const div = document.createElement("div");
        div.classList.add("preview-item");

        let content = "";
        if (file.type.startsWith("image/")) {
            content = `<img src="${e.target.result}" alt="${file.name}">`;
        } else if (file.type === "application/pdf") {
            content = '<div class="pdf-icon">📄</div>';
        }

        div.innerHTML = content;

        if (fileId !== null) {
            div.dataset.fileId = fileId;
        }
        document.getElementById("preview-container").appendChild(div);
    };
    reader.readAsDataURL(file);
}


function handleFiles(files) {
    const previewContainer = document.getElementById("preview-container");

    [...files].forEach(file => {

        const formData = new FormData();
        formData.append("ticket_file", file);

        fetch('/profile/ticket/add-file-ajax/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                // Add file id to hidden input
                const hidden_input = document.getElementById("id_list_input");
                hidden_input.value += "," + String(data.file_id)
                previewFile(file, data.file_id);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('خطا در آپلود فایل: ' + error.message);
            });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");

    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });
    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    fileInput.addEventListener("change", () => {
        handleFiles(fileInput.files);
    });
});


function addDeleteButton(div, fileId) {
    const btn = document.createElement("button");
    btn.classList.add("delete-btn");
    btn.textContent = "✕";

    btn.onclick = function (e) {
        e.stopPropagation();

        if (!fileId) {
            div.remove();
            return;
        }
        removeIdFromHiddenInput(fileId)
        $.get("/profile/ticket/remove-file-ajax/" + fileId, {}).then(re => {
            console.log(re)
        })
        div.remove();
    };

    div.appendChild(btn);
}

function previewFile(file, fileId = null) {
    const reader = new FileReader();

    reader.onload = function (e) {
        const div = document.createElement("div");
        div.classList.add("preview-item");

        let content = "";
        if (file.type.startsWith("image/")) {
            content = `<img src="${e.target.result}" alt="${file.name}">`;
        } else if (file.type === "application/pdf") {
            content = '<div class="pdf-icon">📄</div>';
        }

        div.innerHTML = content;

        if (fileId !== null) {
            div.dataset.fileId = fileId;
        }

        addDeleteButton(div, fileId);

        document.getElementById("preview-container").appendChild(div);
    };

    reader.readAsDataURL(file);
}


function removeIdFromHiddenInput(fileId) {
    const hidden_input = document.getElementById("id_list_input");

    if (hidden_input.value) {
        const ids = hidden_input.value
            .split(',')
            .map(s => s.trim())
            .filter(Boolean);
        console.log(ids)
        const nextIds = ids.filter(id => String(id) !== String(fileId));

        hidden_input.value = nextIds.join(',');
    }
}