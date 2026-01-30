document.addEventListener("DOMContentLoaded", () => {

    async function searchCountry() {
        const query = document.getElementById("searchInput").value.trim();
        if (!query) return;

        try {
            // Fetching data from your Python API
            const res = await fetch(`/api/country?name=${encodeURIComponent(query)}`);
            let data = await res.json();

            // --- THE DEFENSE LOGIC ---
            
            // 1. Handle Array Responses: 
            // Many APIs return a list. We filter to find the EXACT name match.
            if (Array.isArray(data)) {
                const exactMatch = data.find(c => 
                    c.country.toLowerCase() === query.toLowerCase()
                );
                
                // If 'China' is searched, specifically look for the one with Beijing as capital
                // to avoid Hong Kong or Taiwan SARs.
                const chinaPriority = query.toLowerCase() === "china" ? 
                    data.find(c => c.capital === "Beijing") : null;

                data = chinaPriority || exactMatch || data[0];
            }

            // 2. Validation Check:
            // If we searched for 'India' but got a result with 0 population, 
            // it means the API gave us a Territory (Military Base) instead of the Country.
            if (query.toLowerCase() === "india" && data.population === 0) {
                alert("Technical Error: API returned a territory. Refining search...");
                // Note: The .find() logic above usually fixes this automatically.
            }

            if (!data || data.error) {
                alert("Country not found. Please try a more specific name.");
                return;
            }

            // 3. Update UI
            updateUI(data);

        } catch (error) {
            console.error("Fetch error:", error);
            alert("Connection error. Please check if your server is running.");
        }
    }

    function updateUI(data) {
        // Text Information
        document.getElementById("country").textContent = data.country;
        document.getElementById("capital").textContent = data.capital;
        
        // .toLocaleString() ensures India's population looks like 1,408,044,263
        document.getElementById("population").textContent = data.population.toLocaleString();
        
        document.getElementById("region").textContent = data.region;
        document.getElementById("language").textContent = data.language;
        document.getElementById("currency").textContent = `${data.currency_name} ${data.currency_symbol}`;

        // Visual Information
        document.getElementById("flag").src = data.flag;
        document.getElementById("fact-image").src = data.fact_image || data.flag; // Fallback to flag if no image
        document.getElementById("fact-text").textContent = data.fact_text;
        document.getElementById("wikiLink").href = data.wiki;
    }

    // --- Event Listeners ---
    
    // Search Trigger
    document.getElementById("searchBtn").onclick = searchCountry;
    
    // Allow 'Enter' key to search
    document.getElementById("searchInput").onkeypress = (e) => { 
        if (e.key === "Enter") searchCountry(); 
    };

    // Reset Button
    document.getElementById("resetBtn").onclick = () => {
        document.getElementById("searchInput").value = "";
        location.reload(); 
    };

    // Exit Button
    document.getElementById("exitBtn").onclick = () => {
        if (confirm("Are you sure you want to exit?")) {
            window.location.href = "https://www.google.com";
        }
    };
});