async function searchProducts() {
    const query = document.getElementById('searchInput').value;
    if (!query) return;

    // UI Updates
    const btn = document.getElementById('searchBtn');
    const loading = document.getElementById('loading');
    const resultsArea = document.getElementById('resultsArea');

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    loading.classList.remove('hidden');
    resultsArea.classList.add('hidden');
    resultsArea.innerHTML = ''; // Clear previous

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();

        loading.classList.add('hidden');
        resultsArea.classList.remove('hidden');

        // Render sections
        renderPlatform('Amazon', data.amazon, 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg');
        renderPlatform('Flipkart', data.flipkart, 'https://seeklogo.com/images/F/flipkart-logo-C9E637A758-seeklogo.com.png'); // Placeholder logo
        renderPlatform('Meesho', data.meesho, 'https://play-lh.googleusercontent.com/f7E68pTzD2t7i9e5V-7jVb6_iWzFmJ3xW9hX9_3hX9_3hX9_3hX9_3hX9_3'); // Placeholder logo

    } catch (error) {
        console.error('Error:', error);
        alert(`Request failed: ${error.message}`);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-search"></i> <span>Search</span>';
        loading.classList.add('hidden');
    }
}

function renderPlatform(name, products, logoUrl) {
    const resultsArea = document.getElementById('resultsArea');
    const template = document.getElementById('sectionTemplate');
    const clone = template.content.cloneNode(true);

    // Set Header
    clone.querySelector('.platform-name').textContent = name;
    if (logoUrl) clone.querySelector('img').src = logoUrl;

    const grid = clone.querySelector('.products-grid');

    if (!products || products.error) {
        clone.querySelector('.result-count').textContent = "Error";
        clone.querySelector('.result-count').classList.add('bg-red-100', 'text-red-600');

        const errorMsg = document.createElement('div');
        errorMsg.className = 'col-span-full text-center py-8 text-red-500 bg-red-50 rounded-lg';
        errorMsg.innerHTML = `<i class="fas fa-exclamation-circle mb-2"></i><br>Unable to fetch data. Platform might be blocking requests.`;
        grid.appendChild(errorMsg);
        resultsArea.appendChild(clone);
        return;
    }

    if (products.length === 0) {
        clone.querySelector('.result-count').textContent = "0 Results";
        const emptyMsg = document.createElement('div');
        emptyMsg.className = 'col-span-full text-center py-8 text-gray-500 bg-gray-50 rounded-lg';
        emptyMsg.innerHTML = `<i class="fas fa-box-open mb-2"></i><br>No products found.`;
        grid.appendChild(emptyMsg);
        resultsArea.appendChild(clone);
        return;
    }

    clone.querySelector('.result-count').textContent = `${products.length} Results`;

    products.forEach(p => {
        const card = document.createElement('div');
        card.className = 'group relative flex flex-col bg-white rounded-xl border border-gray-100 hover:shadow-2xl transition duration-300 overflow-hidden';

        card.innerHTML = `
            <div class="aspect-square w-full overflow-hidden bg-gray-100 relative">
                <img src="${p.image}" alt="${p.title}" class="h-full w-full object-contain object-center group-hover:scale-105 transition duration-500 p-4">
                <div class="absolute top-2 right-2 bg-brand-500 text-white text-xs font-bold px-2 py-1 rounded shadow-sm">
                    ${p.source}
                </div>
            </div>
            <div class="flex-1 p-4 flex flex-col">
                <h3 class="text-sm font-medium text-gray-900 line-clamp-2 mb-2 min-h-[2.5rem]" title="${p.title}">
                    <a href="${p.link}" target="_blank" class="hover:text-brand-600 transition">
                        ${p.title}
                    </a>
                </h3>
                <div class="mt-auto flex items-center justify-between pt-2 border-t border-gray-50">
                    <p class="text-xl font-extrabold text-brand-600">${p.price}</p>
                    <a href="${p.link}" target="_blank" class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-brand-50 text-brand-600 hover:bg-brand-600 hover:text-white transition duration-300">
                        <i class="fas fa-external-link-alt text-xs"></i>
                    </a>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    resultsArea.appendChild(clone);
}

// Enter key to search
document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchProducts();
    }
});
