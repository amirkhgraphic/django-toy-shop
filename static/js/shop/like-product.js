function toggleLike(productId, userId) {
    if (userId === undefined) {
        alert('you need to log in first')
        return
    }
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const likeBtn = document.getElementById(`product${productId}`);
    fetch(`http://127.0.0.1:8000/api/shop/like/${productId}/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data['detail'] === 'removed') {
                likeBtn.classList.remove('liked-post');
                likeBtn.nextSibling.textContent = +likeBtn.parentElement.innerText - 1
            } else if (data['detail'] === 'created') {
                likeBtn.classList.add('liked-post')
                likeBtn.nextSibling.textContent = +likeBtn.parentElement.innerText + 1
            }
        })
        .catch(() => {
            console.log("something's wrong")
        })
}