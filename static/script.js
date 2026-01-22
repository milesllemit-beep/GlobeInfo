document.addEventListener("DOMContentLoaded", function() {
    console.log("GlobeInfo JS Loaded and Ready"); // Debug check

    const searchBtn = document.getElementById("searchBtn");
    const redoBtn = document.getElementById("redoBtn");
    const exitBtn = document.getElementById("exitBtn");
    const searchInput = document.getElementById("searchInput");

    // Function to fetch and display country data
    async function searchCountry() {
        const countryName = searchInput.value.trim();
        console.log("Attempting search for:", countryName); // Debug check
        
        if (!countryName) {
            alert("Please enter a country name!");
            return;
        }

        try {
            // Using a slightly more flexible search endpoint
            const response = await fetch(`https://restcountries.com/v3.1/name/${countryName}`);
            
            if (!response.ok) {
                throw new Error("Country not found. Please try another name.");
            }

            const data = await response.json();
            const country = data[0];

            // Update Text Info
            const infoList = document.querySelectorAll(".info li");
            if (infoList.length >= 5) {
                infoList[0].innerHTML = `🏳️ <strong>Country:</strong> ${country.name.common}`;
                infoList[1].innerHTML = `🏛️ <strong>Capital:</strong> ${country.capital ? country.capital[0] : 'N/A'}`;
                infoList[2].innerHTML = `👥 <strong>Population:</strong> ${country.population.toLocaleString()}`;
                infoList[3].innerHTML = `🌎 <strong>Region:</strong> ${country.region}`;
                infoList[4].innerHTML = `🗣️ <strong>Language:</strong> ${Object.values(country.languages || {}).join(", ") || 'N/A'}`;
            }

            // Update Flag
            const flagImg = document.querySelector(".flag");
            if (flagImg) flagImg.src = country.flags.svg;

            // Update Currency
            const currencyDiv = document.querySelector(".currency");
            if (currencyDiv && country.currencies) {
                const currencyKey = Object.keys(country.currencies)[0];
                const currencySymbol = country.currencies[currencyKey].symbol || currencyKey;
                currencyDiv.innerText = currencySymbol;
            }

        } catch (error) {
            console.error("Error fetching data:", error);
            alert(error.message);
        }
    }

    // Attach Event Listeners
    if (searchBtn) {
        searchBtn.onclick = searchCountry; // Using .onclick for maximum compatibility
    }

    if (searchInput) {
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") searchCountry();
        });
    }

    if (redoBtn) {
        redoBtn.addEventListener("click", () => {
            searchInput.value = "";
            location.reload(); 
        });
    }

    if (exitBtn) {
        exitBtn.addEventListener("click", () => {
            if (confirm("Are you sure you want to exit?")) {
                window.location.href = "https://www.google.com";
            }
        });
    }
});