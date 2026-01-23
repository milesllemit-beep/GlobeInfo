document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');

    async function handleSearch() {
        const countryName = searchInput.value.trim();
        if (!countryName) return;

        searchBtn.disabled = true;
        searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            const response = await fetch(`/api/country?name=${countryName}`);
            const data = await response.json();

            if (data.error) {
                alert("Country not found! Try again.");
                return;
            }

            // Update Statistics
            document.getElementById('res-country').textContent = data.country;
            document.getElementById('res-capital').textContent = data.capital;
            document.getElementById('res-population').textContent = data.population.toLocaleString();
            document.getElementById('res-region').textContent = data.region;
            document.getElementById('res-language').textContent = data.language;
            document.getElementById('res-currency').textContent = data.currency_name;
            document.getElementById('res-symbol').textContent = data.currency_symbol;
            document.getElementById('flag').src = data.flag;

            // Update Dynamic Fact Section
            document.getElementById('fact-image').src = data.fact_image;
            document.getElementById('fact-text').textContent = data.fact_text;
            document.getElementById('wikiLink').href = `https://en.wikipedia.org/wiki/${data.country}`;

        } catch (error) {
            console.error("Error:", error);
        } finally {
            searchBtn.disabled = false;
            searchBtn.innerHTML = 'Search';
        }
    }

    searchBtn.onclick = handleSearch;
    searchInput.onkeypress = (e) => { if(e.key === 'Enter') handleSearch(); };

    // Reset Button
    document.getElementById('resetBtn').onclick = () => {
        searchInput.value = '';
        location.reload();
    };

    // Exit Button
    document.getElementById('exitBtn').onclick = () => {
        if(confirm("Are you sure you want to exit?")) {
            window.location.href = "https://www.google.com";
        }
    };
});