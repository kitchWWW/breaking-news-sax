console.log("loaded!")

// let SERVER_URL = "https://wapi.brianellissound.com/sound-collage"
let SERVER_URL = "http://0.0.0.0:3009/sound-collage"
// Initialize variables
let mediaRecorder;
let chunks = [];

let statusDiv = document.getElementById("status")




function playAudioWithKey(key){
    setTimeout(function(){
       checkFileExists(key); 
   },3 * 1000)
}


function checkFileExists(timestamp) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // File exists, load and play it
                // var audio = new Audio(SERVER_URL+'/uploads/' + timestamp + '_out.wav');
                document.getElementById("recordingStatus3").style.display = "none"
                document.getElementById("audioElement2").src = SERVER_URL+'/uploads/' + timestamp + '_out.wav'
                document.getElementById("audioElement2").style.display = "block"
            } else {
                // File doesn't exist yet, continue checking
                setTimeout(function() {
                    checkFileExists(timestamp);
                }, 1000); // Adjust the interval as needed (in milliseconds)
            }
        }
    };
    xhr.open('HEAD', SERVER_URL+'/uploads/' + timestamp + '_out.wav', true);
    xhr.send();
}


var STATUS = {
    PLAYING:"playing",
    THINKING:"thinking",
    LISTENING:"listening",
}

var started = false


function startRecording1(){
    startAudioContext()
    document.getElementById("startRecording1").disabled = true
    document.getElementById("recordingStatus1").style.display = "inline"
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(e) {
                chunks.push(e.data);
            }
            mediaRecorder.onstop = function() {
                const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
                chunks = [];
                const audioUrl = URL.createObjectURL(blob);
                document.getElementById('audioElement').src = audioUrl;
                // Send audio data to server
                sendAudioToServer(blob);
            }
            mediaRecorder.start();

            setTimeout(function(){
                mediaRecorder.pause()
                document.getElementById("recordingStatus1").innerHTML = "done!"
                document.getElementById("startRecording2").disabled = false
            },5*1000) 
        })
        .catch(function(err) {
            console.log('The following getUserMedia error occurred: ' + err);
        });
}


function startRecording2(){
    mediaRecorder.resume()
    document.getElementById("startRecording2").disabled = true
    document.getElementById("recordingStatus2").style.display = "inline"
    setTimeout(function(){
        mediaRecorder.pause()
        document.getElementById("recordingStatus2").innerHTML = "done!"
        document.getElementById("startRecording3").disabled = false
    },10*1000) 
}


function startRecording3(){
    mediaRecorder.resume()
    document.getElementById("startRecording3").disabled = true
    document.getElementById("recordingStatus3").style.display = "inline"
    setTimeout(function(){
        mediaRecorder.stop()
        document.getElementById("recordingStatus3").innerHTML = "done! processing..."
        // document.getElementById("startRecording3").disabled = false
    },3*1000) 
}

// Function to send audio data to server
function sendAudioToServer(blob) {
    const formData = new FormData();
    formData.append('audio', blob);

    fetch(SERVER_URL + '/upload_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log('Audio data successfully sent to server:', data);
        playAudioWithKey(data)
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to start the audio context on user touch
function startAudioContext() {
    // Check if the context is already started
    if (window.AudioContext || window.webkitAudioContext) {
        // Create an empty buffer
        var buffer = new AudioBuffer({ length: 1, sampleRate: 44100 });

        // Create an AudioContext
        var audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Create a source node
        var source = audioContext.createBufferSource();

        // Connect the source to the context's destination (speakers)
        source.connect(audioContext.destination);

        // Start the source node
        source.start(0);
    }
}
