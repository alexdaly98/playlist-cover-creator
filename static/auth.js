document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('btn_login').addEventListener('click', initiateSpotifyAuth);
    console.log(1)
    // Check if the user is already logged in
    const accessToken = sessionStorage.getItem('access_token');
    if (accessToken) {
        // User is logged in, proceed with app logic
        checkLoginStatus();
        return; // Exit the function to avoid further checks
    }

    // Check if we are on the redirect URI with an authorization code
    const code = await getAuthorizationCode();
    if (code) {
        await getToken(code);
    }
    checkLoginStatus(); // Check login status if no code is found
});


// Function to check login status and display user profile
function checkLoginStatus() {
    const accessToken = sessionStorage.getItem('access_token');
    const userImage = document.getElementById('user_image');
    const userName = document.getElementById('user_name');

    if (accessToken) {
        fetchUserProfile(); // Fetch profile using async function
    } else {
        userImage.style.display = 'none';
        userName.style.display = 'none';
        document.getElementById('btn_login').style.display = 'inline'; // Show login button if not logged in
    }
}

// Async function to fetch user profile
async function fetchUserProfile() {
    const accessToken = sessionStorage.getItem('access_token');
    if (!accessToken) {
        console.error('No access token found');
        return;
    }

    try {
        const response = await fetch('https://api.spotify.com/v1/me', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user profile');
        }

        const userProfile = await response.json();
        displayUserProfile(userProfile);
    } catch (error) {
        console.error('Error fetching user profile:', error);
    }
}

// Function to display user profile
function displayUserProfile(userProfile) {
    const userName = document.getElementById('user_name');
    const userImage = document.getElementById('user_image');

    if (userProfile) {
        userName.textContent = `Logged in as: ${userProfile.display_name}`;
        userImage.src = userProfile.images[0]?.url || 'https://i0.wp.com/sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png?w=300&ssl=1'; // Provide a default image URL if no profile image is available
        userImage.style.display = 'block'; // Ensure image is visible
        document.getElementById('btn_login').style.display = 'none'; // Hide login button if logged in
    }
}


// PKCE Code Verifier and Code Challenge Generation
const generateRandomString = (length) => {
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const values = crypto.getRandomValues(new Uint8Array(length));
    return values.reduce((acc, x) => acc + possible[x % possible.length], "");
};

const sha256 = async (plain) => {
    const encoder = new TextEncoder();
    const data = encoder.encode(plain);
    return window.crypto.subtle.digest('SHA-256', data);
};

const base64encode = (input) => {
    return btoa(String.fromCharCode(...new Uint8Array(input)))
        .replace(/=/g, '')
        .replace(/\+/g, '-')
        .replace(/\//g, '_');
};

// Request User Authorization
const clientId = '6b28d044e2544b87a3d954a8fe6fdccc';  // Replace with your Spotify app client ID
const redirectUri = 'https://playlist-cover-creator-888428643041.europe-west9.run.app/thumbnail-generator';  // Replace with your app's redirect URI
// const redirectUri = 'http://127.0.0.1:8080/thumbnail-generator';  // Replace with your app's redirect URI
const scope = 'ugc-image-upload playlist-modify-public playlist-modify-private';

const initiateSpotifyAuth = async () => {
    const codeVerifier = generateRandomString(64);
    const hashed = await sha256(codeVerifier);
    const codeChallenge = base64encode(hashed);
    const authUrl = new URL("https://accounts.spotify.com/authorize");

    window.sessionStorage.setItem('code_verifier', codeVerifier);

    const params = {
        response_type: 'code',
        client_id: clientId,
        scope,
        code_challenge_method: 'S256',
        code_challenge: codeChallenge,
        redirect_uri: redirectUri,
    };

    authUrl.search = new URLSearchParams(params).toString();
    window.location.href = authUrl.toString();
};

// Handle OAuth Callback
const getAuthorizationCode = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    return code;
};

const getToken = async code => {

    // stored in the previous step
    let codeVerifier = sessionStorage.getItem('code_verifier');
  
    const payload = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        client_id: clientId,
        grant_type: 'authorization_code',
        code,
        redirect_uri: redirectUri,
        code_verifier: codeVerifier,
      }),
    }
    
    const url = "https://accounts.spotify.com/api/token";
    const body = await fetch(url, payload);
  
    if (!body.ok) {
      alert(
        "You are not authorized. You can create playlist covers but you won't be able to upload them to Spotify here.\n\n" +
        "Send an email to ajmdaly@gmail.com (with the email your Spotify account is related to) to ask for permission."
      );
    }
  
    const response = await body.json();
    sessionStorage.setItem('access_token', response.access_token);
}
  

  