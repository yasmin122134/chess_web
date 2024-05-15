

// openPage.js
document.addEventListener("DOMContentLoaded", function() {

    // Add event listener to the button on the opening page
  const singlePlayerButton = document.getElementById("sp");
    singlePlayerButton.addEventListener('click', startGame);

    const multiPlayerButton = document.getElementById("mp");
    multiPlayerButton.addEventListener('click', startGame);
});





function startGame() {
    // Generate a session ID
    console.log('Starting game')
    generateSession();
    console.log('Session generated2')
    window.location.href = '/web';
}


function generateSession() {
    fetch('/generate_session', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // Store the session ID in a cookie
        document.cookie = `session_id=${data.cookie}`;
    }).then(() => {
        console.log('Session generated1');
    })
    .catch(error => {
        console.error('Error generating session:', error);
    });
}