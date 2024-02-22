function addToCart(productId, cartId = null, quantity = 1) {
    const url = 'http://127.0.0.1:8000/api/cart/cartproduct/create/';
    const formData = new FormData();

    formData.append('product', productId);
    if (cartId !== null) {
        formData.append('cart', cartId);
    }
    formData.append('quantity', quantity);

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': 'Bearer YourAuthToken',  // If authentication is required
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add product to cart');
        }
        return response.json();
    })
    .then(data => {
        console.log('Product added to cart:', data);
        // Handle success, if needed
    })
    .catch(error => {
        console.error('Error adding product to cart:', error.message);
        // Handle error, if needed
    });
}
