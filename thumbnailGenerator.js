
document.addEventListener('DOMContentLoaded', populatePlaylistData);


function populatePlaylistData() {
    const playlist = JSON.parse(sessionStorage.getItem('selectedPlaylist'));

    if (playlist) {
        document.getElementById('playlist_name').textContent = playlist.playlist_name;
        document.getElementById('playlist_image').src = playlist.playlist_image;
        document.getElementById('track_count').textContent = `${playlist.track_count} track(s)`;

        // Fetch and display tracks
        fetchTracks(playlist.id);

        addThumbnailGenerationListener(playlist.id);
    }
}

function fetchTracks(playlistId) {
    fetch(`http://127.0.0.1:5000/tracks/${playlistId}`)
        .then(response => response.json())
        .then(tracks => {
            const tracksList = document.getElementById('tracks-list-thumbnail-page');
            tracksList.innerHTML = ''; // Clear previous tracks

            tracks.forEach(track => {
                const trackDiv = document.createElement('div');
                trackDiv.className = 'track';
                trackDiv.id = 'track-thumbnail';
                trackDiv.innerHTML = `
                    <input type="checkbox" class="track-checkbox" 
                    data-image-url="${track.image_url}" 
                    data-artist="${track.artist}" 
                    data-title="${track.track_name}">
                    <img src="${track.image_url}" alt="${track.track_name}">
                    <div>
                        <div class="track_name">${track.track_name}</div>
                        <div class="track_artist">${track.artist}</div>
                    </div>
                `;
                tracksList.appendChild(trackDiv);
            });
        })
        .catch(error => console.error('Error fetching tracks:', error));
}



function addThumbnailGenerationListener(playlistId) {
    document.getElementById('btn_generate_thumbnail').addEventListener('click', () => {
        const selectedOption = document.querySelector('input[name="thumbnailData"]:checked');
        if (selectedOption) {
            const method = selectedOption.value;
            generateThumbnail(method);
        } else {
            alert('Please select an option to generate a thumbnail.');
        }
    });

    document.getElementById('btn_push_to_spotify').addEventListener('click', async () => {
        const generatedImageUrl = document.getElementById('generated_image').src; // URL of the generated image
        
        const accessToken = sessionStorage.getItem('access_token');
        if (accessToken) {
            if (generatedImageUrl) {
                await uploadPlaylistImageFromUrl(playlistId, generatedImageUrl, accessToken);
            } else {
                console.error('No image generated to upload.');
            }
        } else {
            console.error('Access token is not available.');
            alert('Please log in first.');
        }
    });
}


function generateThumbnail(creation_method) {
    const checkboxes = document.querySelectorAll('.track-checkbox:checked');
    const selectedTracks = Array.from(checkboxes).map(checkbox => ({
        image_url: checkbox.getAttribute('data-image-url'),
        artist: checkbox.getAttribute('data-artist'),
        title: checkbox.getAttribute('data-title')
    }));

    if (selectedTracks.length === 0) {
        alert('Please select at least one track.');
        return;
    }
    
    document.getElementById('loading_widget_generation').style.display = 'block';
    document.getElementById('success_message_generation').style.display = 'none';
    document.getElementById('success_message_upload').style.display = 'none';

    
    // ////////// Skip the fetch call and simulate a successful response with the image URL
    // const simulatedResponse = {
    //     image_url: 'https://i.scdn.co/image/ab67616d0000b273c13ecf7ced29f9982b013314'
    // };

    // // Use the simulated response data
    // const generatedImage = document.getElementById('generated_image');
    // generatedImage.src = simulatedResponse.image_url;
    // generatedImage.style.display = 'block';
    // document.getElementById('btn_push_to_spotify').style.display = 'block';
    // document.getElementById('post_generation').style.display = 'block';

    // document.getElementById('loading_widget_generation').style.display = 'none';
    // document.getElementById('success_message_generation').style.display = 'block';
    // return; 
    // ///////////////////////////////////////////////////////  


    fetch(`http://127.0.0.1:5000/thumbnail/${creation_method}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tracks: selectedTracks })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // Parse the JSON response
        })
        .then(data => {
            if (data && data.image_url) {  // Ensure image_url is present in JSON response
                const generatedImage = document.getElementById('generated_image');
                generatedImage.src = data.image_url;
                generatedImage.style.display = 'block';
                document.getElementById('btn_push_to_spotify').style.display = 'block';
            } else {
                console.error('Invalid data format received');
            }
        })
        .catch(error => console.error('Error generating image:', error))
        .finally(() => {
            document.getElementById('loading_widget_generation').style.display = 'none';
            document.getElementById('success_message_generation').style.display = 'block';
            document.getElementById('post_generation').style.display = 'block';
        });
}


async function uploadPlaylistImageFromUrl(playlistId, imageUrl, accessToken) {
    document.getElementById('loading_widget_upload').style.display = 'block';
    try {
        const response = await fetch('http://127.0.0.1:5000/upload-playlist-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                playlist_id: playlistId,
                image_url: imageUrl,
                access_token: accessToken
            })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('success_message_upload').style.display = 'block';
            console.log(data.message);
            // Update sessionStorage with the new image URL
            let playlist = JSON.parse(sessionStorage.getItem('selectedPlaylist'));
            if (playlist) {
                playlist.playlist_image = imageUrl;
                sessionStorage.setItem('selectedPlaylist', JSON.stringify(playlist));
            }
        } else {
            console.error('Error:', data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
    document.getElementById('loading_widget_upload').style.display = 'none';
}
