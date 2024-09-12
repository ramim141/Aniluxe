function handleSort() {
    const sortOption = document.getElementById('sort-select').value;
    const productContainer = document.querySelector('.grid');
    const products = Array.from(document.querySelectorAll('.product-item'));

    products.sort((a, b) => {
        let aValue, bValue;

        switch (sortOption) {
            case 'price':
                aValue = parseFloat(a.getAttribute('data-price'));
                bValue = parseFloat(b.getAttribute('data-price'));
                return aValue - bValue;
            case 'price_desc':
                aValue = parseFloat(a.getAttribute('data-price'));
                bValue = parseFloat(b.getAttribute('data-price'));
                return bValue - aValue;
            case 'rating':
                aValue = parseFloat(a.getAttribute('data-rating'));
                bValue = parseFloat(b.getAttribute('data-rating'));
                return bValue - aValue;
            case 'popularity':
                aValue = parseFloat(a.getAttribute('data-popularity'));
                bValue = parseFloat(b.getAttribute('data-popularity'));
                return bValue - aValue;
            default:
                return 0;
        }
    });

    // Remove existing products
    productContainer.innerHTML = '';

    // Append sorted products
    products.forEach(product => productContainer.appendChild(product));
}

document.querySelectorAll('.thumbnail').forEach(thumbnail => {
    thumbnail.addEventListener('click', (event) => {
        event.preventDefault();
        const newImageSrc = thumbnail.getAttribute('data-image');
        document.getElementById('main-image').setAttribute('src', newImageSrc);
    });
});

