document.addEventListener('DOMContentLoaded', () => {
    let dropdown = document.querySelector('button#qtyBtn');
    document.querySelector('ul#qtyDropdown').addEventListener('click', (event) => {
        dropdown.innerHTML = event.target.innerHTML;
        document.querySelector('input[name="qty"]').value = dropdown.innerHTML;
    });
});