// Main application functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');
    const closeMobileMenu = document.getElementById('closeMobileMenu');

    mobileMenuBtn.addEventListener('click', function() {
        mobileNav.classList.add('open');
    });

    closeMobileMenu.addEventListener('click', function() {
        mobileNav.classList.remove('open');
    });

    // Initialize map
    const map = L.map('map').setView([-0.5, 34.2], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Simulate flood data
    const floodAreas = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": { "risk": "high", "name": "Bunyala South" },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [34.15, -0.52], [34.17, -0.52],
                        [34.17, -0.50], [34.15, -0.50],
                        [34.15, -0.52]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": { "risk": "moderate", "name": "Bunyala North" },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [34.13, -0.48], [34.15, -0.48],
                        [34.15, -0.46], [34.13, -0.46],
                        [34.13, -0.48]
                    ]]
                }
            }
        ]
    };

    L.geoJSON(floodAreas, {
        style: function(feature) {
            return {
                fillColor: feature.properties.risk === 'high' ? '#D32F2F' : '#FFA000',
                weight: 2,
                opacity: 1,
                color: 'white',
                fillOpacity: 0.7
            };
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`<b>${feature.properties.name}</b><br>Risk: ${feature.properties.risk}`);
        }
    }).addTo(map);

    // Hide loading spinner
    document.querySelector('.map-loading').style.display = 'none';

    // Form submission
    document.getElementById('reportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your report! This data will help protect the community.');
        this.reset();
    });
});