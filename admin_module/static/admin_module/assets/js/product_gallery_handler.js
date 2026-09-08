const fileInput = document.getElementById('fileInput');
const galleryGrid = document.getElementById('galleryGrid');
const addTile = document.getElementById('addTile');
const addTrigger = document.getElementById('addTrigger');

function openPicker() {
    fileInput.click();
}

addTile.addEventListener('click', openPicker);
addTrigger.addEventListener('click', openPicker);

fileInput.addEventListener('change', (e) => {
    [...e.target.files].forEach(file => {
        const url = URL.createObjectURL(file);
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.innerHTML = `
        <img src="${url}" alt="">
        <div class="remove-overlay" title="حذف تصویر">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path><path d="M10 11v6"></path><path d="M14 11v6"></path><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"></path></svg>
        </div>`;
        galleryGrid.insertBefore(item, addTile);
    });
    fileInput.value = '';
});

// remove image on trash click (delegated)
galleryGrid.addEventListener('click', (e) => {
    const overlay = e.target.closest('.remove-overlay');
    if (overlay) {
        overlay.closest('.gallery-item').remove();
    }
});
