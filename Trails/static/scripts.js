// Search functionality with map integration
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const trailResults = document.getElementById('trailResults');

    // Initialize map
    var map = L.map('map').setView([51.505, -0.09], 13); // Example coordinates, adjust based on your app

    // Add OpenStreetMap tiles to the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Function to add markers to map
    function addMarkers(trails) {
        // Clear any existing layers (markers)
        map.eachLayer((layer) => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        // Add markers for each trail
        trails.forEach(trail => {
            const marker = L.marker([trail.latitude, trail.longitude]).addTo(map);
            marker.bindPopup(`<b>${trail.name}</b><br>Location: ${trail.location}<br>Distance: ${trail.distance} km`);
        });

        // Fit map to the markers
        const bounds = trails.map(trail => [trail.latitude, trail.longitude]);
        if (bounds.length > 0) {
            map.fitBounds(bounds);
        }
    }

    // Search form event listener
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const query = searchInput.value;

        // Fetch search results from Flask API
        const response = await fetch(`/search?query=${query}`);
        const results = await response.json();

        // Display search results and add markers on map
        trailResults.innerHTML = results.length
            ? results.map(trail => `<p>${trail.name} - ${trail.difficulty}</p>`).join('')
            : '<p>No trails found.</p>';

        // Add markers for the search results
        addMarkers(results);
    });
});

// Profile update functionality
document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');
    const profileMessage = document.getElementById('profileMessage');

    profileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const bio = document.getElementById('bio').value;
        
        // Simulate profile update
        profileMessage.innerHTML = `<p>Profile updated!<br>Username: ${username}<br>Bio: ${bio}</p>`;
        
        // Clear the form
        profileForm.reset();
    });
});
 