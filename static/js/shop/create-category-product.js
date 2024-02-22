function addCategory() {
    const postForm = document.getElementById('productForm');
    const categoryName = document.getElementById('categoryName').value;
    const categoryThumbnail = document.getElementById('categoryThumbnail').files[0];

    // Clear input fields
    document.getElementById('categoryName').value = '';
    document.getElementById('categoryThumbnail').value = '';

    // Send request to Django API to create category
    const formData = new FormData();
    formData.append('name', categoryName)
    if (categoryThumbnail !== undefined) {
        formData.append('thumbnail', categoryThumbnail)
    }

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch('http://127.0.0.1:8000/api/shop/category/create/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        }
    })
    .then(data => {
        const category = `
        <li style="display: block">
              <img
                  src="${data['thumbnail']}"
                  alt="${data['name']}"
                  height="20px"
                  class="my-2"
              >
              ${data['name']}
        </li>
        `
        const categoriesList = document.getElementById('categoriesList');
        categoriesList.innerHTML += category;

        inputCategory = document.createElement('input');
        inputCategory.hidden = true;
        inputCategory.name = 'category-id';
        inputCategory.defaultValue = `${data['id']}`;
        inputCategory.classList.add('category-id');
        postForm.prepend(inputCategory);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}