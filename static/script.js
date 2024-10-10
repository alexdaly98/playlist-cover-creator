// Fetch and display the user's playlists based on the entered User ID
function getPlaylists() {
    const userId = document.getElementById('user_id_input').value;
    fetch(`playlists/${userId}`)
        .then(response => {
            if (!response.ok) {
                // If response is not ok, throw an error
                alert('Failed to fetch playlists. Please check the User ID and try again.');
            }
            return response.json();
        })
        .then(playlists => {
            sessionStorage.setItem('userIdSearched', userId);
            const playlistsList = document.getElementById('playlists_list');
            playlistsList.innerHTML = ''; // Clear the previous results

            playlists.forEach(playlist => {
                // Create elements
                const playlistDiv = document.createElement('div');
                playlistDiv.className = 'playlist';
                playlistDiv.dataset.playlistId = playlist.id; // Use data attribute to store playlist id

                const playlistSummaryDiv = document.createElement('div');
                playlistSummaryDiv.className = 'summary';

                const playlistImage = document.createElement('img');
                playlistImage.src = playlist.image_url;
                playlistImage.alt = playlist.name;
                playlistImage.width = 100;

                const nameDiv = document.createElement('div');
                nameDiv.className = 'name';
                nameDiv.textContent = playlist.name;

                const trackCountDiv = document.createElement('div');
                trackCountDiv.className = 'track_count';
                trackCountDiv.textContent = `${playlist.track_count} track(s)`;

                const playlistButtonsDiv = document.createElement('div');
                playlistButtonsDiv.className = 'buttons_div';

                const trackShowButton = document.createElement('button');
                trackShowButton.textContent = "Show/Hide tracks";
                trackShowButton.className = "button_tracks";
                // Add event listener to the button
                trackShowButton.addEventListener('click', () => showTracks(playlist.id));

                const playlistSelectButton = document.createElement('button');
                playlistSelectButton.textContent = "Select playlist";
                playlistSelectButton.className = "button_select";
                playlistSelectButton.addEventListener('click', () => selectPlaylist(playlist));

                const trackShowButtonDiv = document.createElement('div');
                trackShowButtonDiv.appendChild(trackShowButton);

                const playlistSelectButtonDiv = document.createElement('div');
                playlistSelectButtonDiv.appendChild(playlistSelectButton);

                playlistButtonsDiv.appendChild(playlistSelectButtonDiv);
                playlistButtonsDiv.appendChild(trackShowButtonDiv);

                // Append elements to playlistDiv
                playlistSummaryDiv.appendChild(playlistImage);
                playlistSummaryDiv.appendChild(nameDiv);
                playlistSummaryDiv.appendChild(trackCountDiv);
                playlistSummaryDiv.appendChild(playlistButtonsDiv);

                playlistDiv.appendChild(playlistSummaryDiv);
                playlistsList.appendChild(playlistDiv);
            });
        })
        .catch(error => console.error('Error fetching playlists:', error));
}

// Fetch and display tracks for a specific playlist
function showTracks(playlistId) {
    fetch(`tracks/${playlistId}`)
        .then(response => response.json())
        .then(tracks => {
            const playlistDiv = document.querySelector(`.playlist[data-playlist-id='${playlistId}']`);
            let tracksDiv = playlistDiv.querySelector('.tracks_list');

            // If the tracks list is already shown, remove it
            if (tracksDiv) {
                tracksDiv.remove();
                return;
            }

            // Create a new tracks list if it doesn't exist
            tracksDiv = document.createElement('div');
            tracksDiv.className = 'tracks_list';
            tracksDiv.innerHTML = '<h3>Tracks</h3>';

            tracks.forEach(track => {
                const trackDiv = document.createElement('div');
                trackDiv.className = 'track';
                trackDiv.innerHTML = `
                    <img src="${track.image_url}" alt="${track.name}">
                    <div>
                        <div class="track_name">${track.name}</div>
                        <div class="track_artist">${track.artist}</div>
                    </div>
                `;
                tracksDiv.appendChild(trackDiv);
            });

            playlistDiv.appendChild(tracksDiv);
        })
        .catch(error => console.error('Error fetching tracks:', error));
}

function selectPlaylist(playlist) {
    // Save the selected playlist data
    sessionStorage.setItem('selectedPlaylist', JSON.stringify(playlist));

    // Redirect to thumbnailGenerator.html
    window.location.href = '/thumbnail-generator';
}
