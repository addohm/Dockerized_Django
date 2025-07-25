document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.addEventListener('change', function (event) {
            const [file] = event.target.files;
            const preview = document.getElementById('image-preview');
            if (file && preview) {
                preview.src = URL.createObjectURL(file);
            }
        });
    }
});