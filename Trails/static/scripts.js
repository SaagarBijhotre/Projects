// Search

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const trailResults = document.getElementById('trailResults');

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = searchInput.value.toLowerCase();
        
        // Simulate search results
        const trails = [
            'Sunny Trail - Easy',
            'Mountain Path - Moderate',
            'Forest Walk - Hard'
        ];

        const results = trails.filter(trail => trail.toLowerCase().includes(query));

        // Display results
        trailResults.innerHTML = results.length
            ? results.map(trail => `<p>${trail}</p>`).join('')
            : '<p>No trails found.</p>';
    });
});
// Profile

document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');
    const profileMessage = document.getElementById('profileMessage');

    profileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const bio = document.getElementById('bio').value;
        
        // Simulate profile update
        // In a real application, you would send this data to a server
        profileMessage.innerHTML = `<p>Profile updated!<br>Username: ${username}<br>Bio: ${bio}</p>`;
        
        // Clear the form
        profileForm.reset();
    });
});
// Flask

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const trailResults = document.getElementById('trailResults');

    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const query = searchInput.value;

        // Fetch search results from Flask API
        const response = await fetch(`/search?query=${query}`);
        const results = await response.json();

        // Display results
        trailResults.innerHTML = results.length
            ? results.map(trail => `<p>${trail.name} - ${trail.difficulty}</p>`).join('')
            : '<p>No trails found.</p>';
    });
});

