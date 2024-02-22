function deleteProductCart(cartProductId) {
    const url = `http://127.0.0.1:8000/api/cart/cartproduct/delete/${cartProductId}`;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
            // Add any additional headers if needed
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete product from cart');
        }
        const tr = document.querySelector(`tr[data-product-id="${cartProductId}"]`);
        if (tr) {
            tr.remove();
        }
        // Handle success, if needed
    })
    .catch(error => {
        console.error('Error deleting product from cart:', error.message);
        // Handle error, if needed
    });
}