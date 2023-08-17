document.addEventListener('DOMContentLoaded', () => {
    let dropdown = document.querySelector('button.dropdown-toggle');
    document.querySelector('ul.dropdown-menu').addEventListener('click', (event) => {
        dropdown.innerHTML = event.target.innerHTML;
        document.querySelector('input[name="qty"]').value = dropdown.innerHTML;
    });
});