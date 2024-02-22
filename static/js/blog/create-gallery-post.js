function addGallery(postId) {
    const fileInput = document.getElementById('galleryFile');
    const galleryList = document.getElementById('galleryList');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // Check if files are selected
    if (fileInput.files && fileInput.files.length > 0) {
        // Loop through each selected file
        for (let i = 0; i < fileInput.files.length; i++) {
            const file = fileInput.files[i];

            const formData = new FormData();
            formData.append('file', file);
            formData.append('post_id', postId);

            fetch('http://127.0.0.1:8000/api/blog/gallery/create/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData
            }).then(response => {
                if (response.ok) {
                    const reader = new FileReader();
                    let data = response.json().then(
                        data => {
                            reader.onload = function(e) {
                                // Display the selected image
                                const image = `<li data-gallery-id="${data['id']}" style="display: inline; margin-right: 5px;">
                                    <span style="cursor: pointer" onclick=deleteGallery(${data['id']})>&times;</span>
                                    <img src="${e.target.result}" alt="Gallery Item" height="100">
                                </li>`;
                                galleryList.innerHTML += image;
                            };

                            // Read the image file
                            reader.readAsDataURL(file);
                        }
                    )
                } else {
                    // Error handling for failed deletion
                    console.error('Failed:', response.statusText);
                }
            })
        }
    }
    fileInput.value = '';
}