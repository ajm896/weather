// Weather data fetching and display script
// replace with your real endpoint
const API_URL = 'http://127.0.0.1:8000/api/weather';

fetch(API_URL)
    .then(res => {
        if (!res.ok) throw new Error(res.statusText);
        return res.text(); // Get as text first
    })
    .then(textData => {
        // Parse JSON manually to handle potential string responses
        let data;
        try {
            data = typeof textData === 'string' ? JSON.parse(textData) : textData;
        } catch (e) {
            throw new Error('Invalid JSON response');
        }

        // find the container…
        const out = document.getElementById('weather');

        // Clear loading message
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
                periodName.textContent = f.name;
                periodName.className = 'text-xl font-semibold text-white mb-2';

                const temperature = document.createElement('div');
                temperature.textContent = `${f.temperature}°F`;
                temperature.className = 'text-3xl font-bold text-white mb-2';

                const shortForecast = document.createElement('p');
                shortForecast.textContent = f.shortForecast || f.detailedForecast || 'No forecast available';
                shortForecast.className = 'text-white/80 text-sm';

                // Add wind info if available
                if (f.windSpeed && f.windDirection) {
                    const windInfo = document.createElement('div');
                    windInfo.textContent = `Wind: ${f.windSpeed} ${f.windDirection}`;
                    windInfo.className = 'text-white/70 text-xs mt-2';
                    card.appendChild(windInfo);
                }

                // Assemble the card
                card.appendChild(periodName);
                card.appendChild(temperature);
                card.appendChild(shortForecast);

                gridContainer.appendChild(card);
            });

            out.appendChild(gridContainer);
        } else {
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
    })
    .catch(err => {
        const out = document.getElementById('weather');
        out.innerHTML = '';

        const errorContainer = document.createElement('div');
        errorContainer.className = 'bg-red-500/20 backdrop-blur-md rounded-lg p-6 shadow-lg border border-red-500/30 max-w-md mx-auto';

        const errorIcon = document.createElement('div');
        errorIcon.innerHTML = '⚠️';
        errorIcon.className = 'text-4xl text-center mb-4';

        const errorTitle = document.createElement('h3');
        errorTitle.textContent = 'Error Loading Weather Data';
        errorTitle.className = 'text-xl font-semibold text-white mb-2 text-center';

        const errorMessage = document.createElement('p');
        errorMessage.textContent = err.message;
        errorMessage.className = 'text-white/80 text-center';

        errorContainer.appendChild(errorIcon);
        errorContainer.appendChild(errorTitle);
        errorContainer.appendChild(errorMessage);
        out.appendChild(errorContainer);

        console.error(err);
    });
