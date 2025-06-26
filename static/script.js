"use strict";
// Weather data fetching and display script
// replace with your real endpoint
const API_URL = 'http://weather-api.localhost/v1/api/weather';
let currentLocation = 'home'; // Default location
async function fetchWeatherData(location) {
    const weatherContainer = document.getElementById('weather');
    // Show loading state
    if (!weatherContainer) {
        console.error("Weather container element not found.");
        return;
    }
    weatherContainer.innerHTML = `
        <div class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
            </svg>
            Loading weather data for ${location}...
        </div>
    `;
    try {
        const res = await fetch(`${API_URL}/${location}`);
        if (!res.ok)
            throw new Error(res.statusText);
        const textData = await res.text(); // Get as text first
        // Parse JSON manually to handle potential string responses
        let data;
        try {
            data = typeof textData === 'string' ? JSON.parse(textData) : textData;
        }
        catch (e) {
            throw new Error('Invalid JSON response');
        }
        // find the container…
        const out = document.getElementById('weather');
        // Clear loading message
        if (!out) {
            console.error("Weather container element not found.");
            return;
        }
        out.innerHTML = '';
        // Access the periods array from weatherData
        let forecast = data.weatherData?.periods;
        if (Array.isArray(forecast)) {
            // Create a grid container for the forecast cards
            const gridContainer = document.createElement('div');
            gridContainer.className = 'grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4';
            forecast.forEach((f, index) => {
                console.log('Period:', f);
                // Create forecast card
                const card = document.createElement('div');
                card.id = 'period_' + f.name;
                card.className = 'bg-white/10 backdrop-blur-md rounded-lg p-6 shadow-lg border border-white/20 hover:bg-white/20 transition-all duration-300';
                // Create card content
                const periodName = document.createElement('h3');
                periodName.textContent = f.name; // Display name and date
                periodName.className = 'text-xl font-semibold text-white mb-2';
                // Create card content
                const periodDate = document.createElement('p');
                periodDate.textContent = f.startTime.split('T')[0]; // Display date
                periodDate.className = 'text-sm text-white/80 mb-2';
                const temperature = document.createElement('div');
                temperature.textContent = `${f.temperature}°F`;
                temperature.className = 'text-3xl font-bold text-white mb-2';
                const shortForecast = document.createElement('p');
                shortForecast.textContent = f.shortForecast || f.detailedForecast || 'No forecast available';
                shortForecast.className = 'text-white/80 text-sm';
                // Add icon if available
                if (f.icon) {
                    const icon = document.createElement('img');
                    icon.src = f.icon;
                    icon.alt = f.name;
                    icon.className = 'w-12 h-12 mb-2';
                    card.appendChild(icon);
                }
                // Assemble the card
                card.appendChild(periodName);
                card.appendChild(periodDate);
                card.appendChild(temperature);
                card.appendChild(shortForecast);
                // Add wind info if available
                if (f.windSpeed && f.windDirection) {
                    const windInfo = document.createElement('div');
                    windInfo.textContent = `Wind: ${f.windSpeed} ${f.windDirection}`;
                    windInfo.className = 'text-white/70 text-xs mt-2';
                    card.appendChild(windInfo);
                }
                gridContainer.appendChild(card);
            });
            out.appendChild(gridContainer);
        }
        else {
            // If not an array, display the raw data for debugging with nice styling
            const debugContainer = document.createElement('div');
            debugContainer.className = 'bg-white/10 backdrop-blur-md rounded-lg p-6 shadow-lg border border-white/20 max-w-4xl mx-auto';
            const debugTitle = document.createElement('h3');
            debugTitle.textContent = 'Debug Data';
            debugTitle.className = 'text-xl font-semibold text-white mb-4';
            const debugContent = document.createElement('pre');
            debugContent.textContent = JSON.stringify(data, null, 2);
            debugContent.className = 'text-white/80 text-sm overflow-auto bg-black/20 rounded p-4';
            debugContainer.appendChild(debugTitle);
            debugContainer.appendChild(debugContent);
            out.appendChild(debugContainer);
        }
    }
    catch (err) {
        const out = document.getElementById('weather');
        if (out) {
            out.innerHTML = '';
        }
        const errorContainer = document.createElement('div');
        errorContainer.className = 'bg-red-500/20 backdrop-blur-md rounded-lg p-6 shadow-lg border border-red-500/30 max-w-md mx-auto';
        const errorIcon = document.createElement('div');
        errorIcon.innerHTML = '⚠️';
        errorIcon.className = 'text-4xl text-center mb-4';
        const errorTitle = document.createElement('h3');
        errorTitle.textContent = 'Error Loading Weather Data';
        errorTitle.className = 'text-xl font-semibold text-white mb-2 text-center';
        const errorMessage = document.createElement('p');
        errorMessage.textContent = (err instanceof Error) ? err.message : String(err);
        errorMessage.className = 'text-white/80 text-center';
        errorContainer.appendChild(errorIcon);
        errorContainer.appendChild(errorTitle);
        errorContainer.appendChild(errorMessage);
        if (out) {
            out.appendChild(errorContainer);
        }
        console.error(err);
    }
}
// Initialize the page
document.addEventListener('DOMContentLoaded', function () {
    const locationSelect = document.getElementById('location-select');
    const updateButton = document.getElementById('fetch-weather-button');
    // Set up event listener for location changes
    if (locationSelect) {
        locationSelect.addEventListener('change', function () {
            currentLocation = this.value;
            fetchWeatherData(currentLocation);
        });
    }
    else {
        console.error("Location select element not found.");
    }
    if (updateButton) {
        updateButton.addEventListener('click', async function () {
            try {
                const res = await fetch(`${API_URL}/update`);
                if (!res.ok)
                    throw new Error(res.statusText);
                document.location.reload();
            }
            catch (err) {
                console.error('Error updating weather data:', err);
                alert('Failed to update weather data. Please try again later.');
            }
        });
    }
    else {
        console.error("Fetch weather button element not found.");
    }
    // Load initial weather data
    fetchWeatherData(currentLocation);
});
