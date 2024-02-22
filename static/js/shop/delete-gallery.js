function deleteGallery(galleryId) {
    // Construct the URL with query parameters
    const url = `http://127.0.0.1:8000/api/shop/gallery/delete/${galleryId}`;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    // Send a DELETE request using fetch()
    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
            // Add any additional headers if needed
        },
    })
    .then(response => {
        if (response.ok) {
            // Remove the corresponding HTML element
            const listItem = document.querySelector(`#galleryList li[data-gallery-id="${galleryId}"]`);
            if (listItem) {
                listItem.remove();
            }
        } else {
            // Error handling for failed deletion
            console.error('Failed to delete CategoryPost:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}