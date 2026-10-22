let searchTimeout;
const searchInput = document.getElementById('universalSearch');
const searchResults = document.getElementById('searchResults');

searchInput.addEventListener('input', function(e) {
    const query = e.target.value.trim();
    
    // Clear previous timeout
    clearTimeout(searchTimeout);
    
    // Hide results if query is empty
    if (!query) {
        searchResults.style.display = 'none';
        return;
    }
    
    // Set new timeout for search
    searchTimeout = setTimeout(() => {
        performSearch(query);
    }, 300); // 300ms delay to prevent too many requests
});

async function performSearch(query) {
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No results found</div>';
        } else {
            searchResults.innerHTML = data.results.map(result => `
                <div class="search-result-item" data-type="${result.type}" data-id="${result.id}">
                    <div class="result-header">
                        <span class="result-type">${result.type}</span>
                        <span class="result-id">${result.id}</span>
                    </div>
                    <div class="result-content">
                        ${result.title}
                    </div>
                    ${result.subtitle ? `<div class="result-subtitle">${result.subtitle}</div>` : ''}
                </div>
            `).join('');
        }
        
        searchResults.style.display = 'block';
        
        // Add click handlers to results
        document.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', () => {
                const type = item.dataset.type;
                const id = item.dataset.id;
                navigateToResult(type, id);
            });
        });
    } catch (error) {
        console.error('Search error:', error);
        searchResults.innerHTML = '<div class="error">Error performing search</div>';
    }
}

function navigateToResult(type, id) {
    switch (type) {
        case 'customer':
            window.location.href = `/customers/${id}`;
            break;
        case 'vehicle':
            window.location.href = `/cars/${id}`;
            break;
        case 'part':
            window.location.href = `/parts/${id}`;
            break;
        case 'bill':
            window.location.href = `/bills/${id}`;
            break;
    }
}

// Close search results when clicking outside
document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.style.display = 'none';
    }
}); 