function parsePrice(priceString) {
    if (!priceString) return Infinity;
    const digits = priceString.replace(/\D/g, '');
    return digits ? parseInt(digits, 10) : Infinity;
}

function clearSearch() {
    const input = document.getElementById('searchInput');
    input.value = '';
    input.focus();
    document.getElementById('clearBtn').classList.add('hidden');
}

document.getElementById('searchInput').addEventListener('input', function(e) {
    const clearBtn = document.getElementById('clearBtn');
    if (e.target.value.length > 0) {
        clearBtn.classList.remove('hidden');
    } else {
        clearBtn.classList.add('hidden');
    }
});

async function searchProducts() {
    const query = document.getElementById('searchInput').value;
    const pincodeElement = document.getElementById('pincodeInput');
    const pincode = pincodeElement ? pincodeElement.value : '';
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
    document.getElementById('recommendationArea').classList.add('hidden');

    try {
        let url = `/api/search?q=${encodeURIComponent(query)}`;
        if (pincode) {
            url += `&pincode=${encodeURIComponent(pincode)}`;
        }
        const response = await fetch(url);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();

        loading.classList.add('hidden');
        resultsArea.classList.remove('hidden');

        // Smart Recommendation Logic
        const recommendationArea = document.getElementById('recommendationArea');
        recommendationArea.innerHTML = ''; // clear previous

        let allProducts = [];
        if (data.amazon && Array.isArray(data.amazon) && data.amazon.length > 0) allProducts.push(...data.amazon);
        if (data.flipkart && Array.isArray(data.flipkart) && data.flipkart.length > 0) allProducts.push(...data.flipkart);
        if (data.meesho && Array.isArray(data.meesho) && data.meesho.length > 0) allProducts.push(...data.meesho);

        if (allProducts.length > 0) {
            let bestProduct = allProducts[0];
            let minPrice = parsePrice(bestProduct.price);

            for (let i = 1; i < allProducts.length; i++) {
                const currentPrice = parsePrice(allProducts[i].price);
                if (currentPrice < minPrice) {
                    minPrice = currentPrice;
                    bestProduct = allProducts[i];
                }
            }

            if (minPrice !== Infinity) {
                recommendationArea.classList.remove('hidden');
                recommendationArea.innerHTML = `
                    <div class="bg-gradient-to-r from-green-50 to-emerald-100 border border-green-200 rounded-2xl p-6 shadow-lg relative overflow-hidden">
                        <div class="absolute top-0 right-0 p-4 opacity-10">
                            <i class="fas fa-crown text-6xl text-green-600"></i>
                        </div>
                        <div class="relative z-10 flex flex-col sm:flex-row items-center gap-6">
                            <div class="w-32 h-32 flex-shrink-0 bg-white rounded-xl p-2 shadow-sm">
                                <img src="${bestProduct.image}" alt="${bestProduct.title}" class="w-full h-full object-contain">
                            </div>
                            <div class="flex-1">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">Best Price Pick</span>
                                    <span class="text-sm font-semibold text-gray-500">on ${bestProduct.source}</span>
                                </div>
                                <h3 class="text-xl font-bold text-gray-900 mb-2 line-clamp-2" title="${bestProduct.title}">
                                    ${bestProduct.title}
                                </h3>
                                <div class="flex items-center gap-4">
                                    <span class="text-3xl font-extrabold text-green-700">${bestProduct.price}</span>
                                    <a href="${bestProduct.link}" target="_blank" class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-6 rounded-lg transition shadow-md flex items-center gap-2">
                                        View Deal <i class="fas fa-arrow-right text-sm"></i>
                                    </a>
                                </div>
                                <p class="text-sm text-green-800 mt-3 font-medium flex items-start gap-2">
                                    <i class="fas fa-lightbulb mt-1"></i>
                                    Tip: Check for additional delivery costs and available bank card discounts on the platform before purchasing.
                                </p>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                 recommendationArea.classList.add('hidden');
            }
        } else {
            recommendationArea.classList.add('hidden');
        }

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
        card.className = 'group relative flex flex-col bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition duration-300 overflow-hidden';

        card.innerHTML = `
            <div class="aspect-square w-full overflow-hidden bg-gray-50 relative p-6">
                <img src="${p.image}" alt="${p.title}" class="h-full w-full object-contain object-center group-hover:scale-110 transition duration-500 drop-shadow-md">
                <div class="absolute top-3 right-3 bg-brand-600 text-white text-[10px] uppercase font-extrabold px-2.5 py-1 rounded-md shadow-sm tracking-wider">
                    ${p.source}
                </div>
            </div>
            <div class="flex-1 p-5 flex flex-col">
                <h3 class="text-base font-semibold text-gray-800 line-clamp-2 mb-3 min-h-[3rem] leading-tight" title="${p.title}">
                    <a href="${p.link}" target="_blank" class="hover:text-brand-600 transition">
                        ${p.title}
                    </a>
                </h3>
                <div class="mt-auto flex items-center justify-between pt-3 border-t border-gray-100">
                    <p class="text-2xl font-black text-brand-600">${p.price}</p>
                    <a href="${p.link}" target="_blank" class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-brand-50 text-brand-600 hover:bg-brand-600 hover:text-white transition duration-300 shadow-sm hover:shadow-md">
                        <i class="fas fa-arrow-up-right-from-square text-sm"></i>
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
