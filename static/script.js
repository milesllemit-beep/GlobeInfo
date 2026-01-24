document.addEventListener("DOMContentLoaded", () => {

    async function searchCountry() {
        const name = document.getElementById("searchInput").value.trim();
        if (!name) return;

        const res = await fetch(`/api/country?name=${name}`);
        const data = await res.json();

        if (data.error) {
            alert("Country not found");
            return;
        }

        document.getElementById("country").textContent = data.country;
        document.getElementById("capital").textContent = data.capital;
        document.getElementById("population").textContent = data.population.toLocaleString();
        document.getElementById("region").textContent = data.region;
        document.getElementById("language").textContent = data.language;
        document.getElementById("currency").textContent =
            data.currency_name + " " + data.currency_symbol;

        document.getElementById("flag").src = data.flag;

        document.getElementById("fact-image").src = data.fact_image;
        document.getElementById("fact-text").textContent = data.fact_text;
        document.getElementById("wikiLink").href = data.wiki;
    }

    document.getElementById("searchBtn").onclick = searchCountry;
    document.getElementById("searchInput").onkeypress = e => {
        if (e.key === "Enter") searchCountry();
    };

    // ✅ BUTTONS KEPT AND FUNCTIONAL
    document.getElementById("resetBtn").onclick = () => location.reload();
    document.getElementById("exitBtn").onclick = () => {
        if (confirm("Are you sure you want to exit?")) {
            window.location.href = "https://www.google.com";
        }
    };
});
