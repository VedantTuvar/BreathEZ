const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  themeToggle.innerHTML = document.body.classList.contains("dark")
    ? '<i class="fa-solid fa-moon"></i>'
    : '<i class="fa-solid fa-sun"></i>';
});

const cityData = {
  Morristown: {
    AQI: 95,
    PM25: "Moderate (45 µg/m³)",
    PM10: "Good (30 µg/m³)",
    Weather: "Clear, 20°C",
  },
  Bronx: {
    AQI: 142,
    PM25: "Unhealthy (90 µg/m³)",
    PM10: "Moderate (60 µg/m³)",
    Weather: "Hazy, 25°C",
  },
};

const locationDetails = document.getElementById("locationDetails");

function showCityDetails(city) {
  const data = cityData[city];
  locationDetails.classList.add("active");
  locationDetails.innerHTML = `
        <div class="city-info">
          <h3>${city}</h3>
          <p><strong>AQI:</strong> ${data.AQI}</p>
          <p><strong>PM2.5:</strong> ${data.PM25}</p>
          <p><strong>PM10:</strong> ${data.PM10}</p>
          <p><strong>Weather:</strong> ${data.Weather}</p>
        </div>
    `;
}

const liveButton = document.querySelector(".live-btn");
liveButton.addEventListener("click", () => {
  alert("Fetching latest live air quality data...");
});

window.addEventListener("load", () => {
  window.scrollTo(0, 0);
});

document.addEventListener("DOMContentLoaded", () => {
  // Card animation logic
  const cards = document.querySelectorAll(".tip-card");
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 150 * index);
  });

  // ===================================
  //  LEAFLET MAP INTEGRATION START
  // ===================================

  // FIX: Manually set the path for Leaflet marker icons.
  // This is crucial when using local Leaflet files.
  if (typeof L !== "undefined") {
    L.Icon.Default.imagePath = "./leaflet-dist/images/";

    // 1. Initialize map
    const airQualityMap = L.map("map").setView([40.85, -73.9], 10); // Center: approx. Morristown/Bronx area

    // 2. Add OpenStreetMap tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(airQualityMap);

    // 3. Define city data for the map
    const cities = [
      {
        name: "Morristown",
        coords: [40.7967, -74.4815],
        aqi: 42,
        status: "Good",
      },
      {
        name: "Bronx",
        coords: [40.8448, -73.8648],
        aqi: 78,
        status: "Moderate",
      },
    ];

    // 4. Add markers for each city and bind popups
    cities.forEach((city) => {
      const marker = L.marker(city.coords).addTo(airQualityMap);

      // Customize the popup content
      const popupContent = `
                <b>${city.name}</b><br>
                AQI: ${city.aqi} (${city.status})
            `;

      marker.bindPopup(popupContent);

      // Add a click listener to the marker to update the Location Details section
      marker.on("click", function () {
        showCityDetails(city.name);
      });
    });
  }
  // ===================================
  //  LEAFLET MAP INTEGRATION END
  // ===================================
});

// Chart initialization logic
const chartColors = {
  aqi: "#f87171",
  pm10: "#facc15",
  pm25: "#fb923c",
};

function generateData() {
  return Array.from({ length: 10 }, () => Math.floor(Math.random() * 180));
}

function createChart(id, label) {
  // Check if Chart is available globally (from the CDN)
  if (typeof Chart !== "undefined" && document.getElementById(id)) {
    new Chart(document.getElementById(id), {
      type: "line",
      data: {
        labels: [
          "09:39",
          "11:39",
          "13:39",
          "15:39",
          "17:39",
          "19:39",
          "21:39",
          "23:39",
          "01:39",
          "03:39",
        ],
        datasets: [
          {
            label: "NO2",
            borderColor: chartColors.aqi,
            data: generateData(),
            fill: false,
            tension: 0.3,
          },
          {
            label: "Ozone",
            borderColor: chartColors.pm10,
            data: generateData(),
            fill: false,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: true, position: "bottom" },
          title: {
            display: true,
            text: label,
            font: { size: 14, weight: "bold" },
          },
        },
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  }
}

createChart("chart1", "No2 Before");
createChart("chart2", "No2 After");
createChart("chart3", "Ozone Before");
createChart("chart4", "Ozone After");
createChart("chart5", "PM 2.5");

// Scroll animation logic
window.addEventListener("scroll", () => {
  const sections = document.querySelectorAll(
    ".aqi-card, .pollutant-card, .group-card"
  );
  sections.forEach((section) => {
    const position = section.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;
    if (position < windowHeight - 100) {
      section.classList.add("visible");
    }
  });
});
