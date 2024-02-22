function deleteCategory(productId, categoryId) {
    // Construct the URL with query parameters
    const url = `http://127.0.0.1:8000/api/shop/category/delete/?product_id=${productId}&category_id=${categoryId}`;
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
            const listItem = document.querySelector(`#categoriesList li[data-category-id="${categoryId}"]`);
            if (listItem) {
                listItem.remove();
            }
        } else console.error('Failed to delete CategoryPost:', response.statusText);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}