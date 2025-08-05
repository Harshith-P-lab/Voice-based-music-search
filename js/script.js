// Function to go back to the previous page
function goBack() {
  window.history.back();
}

function togglePlay() {
  if (audioPlayer.paused) {
    audioPlayer.play(); // Play the audio
    playPauseButton.classList.add('playing');
    playPauseButton.classList.remove('paused');
  } else {
    audioPlayer.pause(); // Pause the audio
    playPauseButton.classList.add('paused');
    playPauseButton.classList.remove('playing');
  }
}


// Function to show credits modal
function showCredits() {
  document.getElementById('credits-modal').style.display = 'flex';
}

// Function to close credits modal
function closeCredits() {
  document.getElementById('credits-modal').style.display = 'none';
}

// Placeholder function for audio search
function searchByAudio() {
  alert("Listening for your input!");
}
function showMore() {
  alert("More features coming soon!");
}

function playSong() {
  alert("Playing song...");
}

function pauseSong() {
  alert("Pausing song...");
}
// Function to start listening and proceed to the next page
function startListening(event) {
  event.preventDefault(); // Prevent default form submission

  // Display a loading message in the textarea
  document.getElementById('output-display').value = "Listening for the song... Please wait.";

  // Call the Flask backend using fetch
  fetch("/process-audio", {
    method: "POST",
  })
  .then(response => response.json())
  .then(data => {
    // Display the result in the textarea
    document.getElementById('output-display').value = data.message;

    // If the message contains 'Playing', it means a song is matched
    if (data.song_title) {
      // Redirect to the index3.html page with the song title
      setTimeout(() => {
        window.location.href = '/index3';
      }, 2000); // Adding a small delay to show the result
    } else {
      // If no song is found, stay on index2 and show the "Song not found" message
      setTimeout(() => {
        window.location.href = '/next';  // Go back to index2 and display message
      }, 2000);  // Adding a small delay to show the result
    }
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById('output-display').value = "Error occurred while searching.";
  });
}
