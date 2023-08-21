document.addEventListener('DOMContentLoaded',  () => {
    if (location.pathname == "/") {
        let searchInput = document.querySelector('input[type="search"]');
        let originalContent = document.querySelector('div.row').innerHTML;

        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
        });

        searchInput.addEventListener('input', async () => {
            let response = await fetch("/search?q=" + searchInput.value);
            let items = await response.json();
            let html = ``;
            for (let id in items) {
                html += `
                <div class="col">
                    <div class="card h-100">
                        <img src="/${items[id].image_path}" class="card-img-top" alt="{{ item.title }}">
                        <div class="card-body">
                            <h5 class="card-title">${items[id].title}</h5>
                            <p class="card-text">${items[id].description}</p>
                            <p class="card-text">Price: ${formatter.format(items[id].price) }</p>
                            <a href="/item/${items[id].id}" class="stretched-link" type="hidden"></a>
                        </div>
                    </div>
                </div>
                `;
            }
            if (searchInput.value)
                document.querySelector('div.row').innerHTML = html;
            else
                document.querySelector('div.row').innerHTML = originalContent;
        });
    }
});