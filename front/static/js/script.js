let mediaRecorder;
let audioChunks = [];
let startTime;
let timerInterval;
let elapsedRecordingTime = 0;

document.getElementById('start-recording').addEventListener('click', startRecording);
document.getElementById('stop-recording').addEventListener('click', stopRecording);

async function startRecording() {
    document.getElementById('recording-status').innerHTML = '<span id="recording-dot" class="recording"></span> Recording...';
    document.getElementById('recording-dot').style.display = 'inline-block';

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstart = () => {
            document.getElementById('recording-status').innerHTML = '<span id="recording-dot" class="recording"></span> Recording...';
            startTime = new Date();
            startTimer();
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];
            const formData = new FormData();
            formData.append('file', audioBlob, 'temp.wav');

            try {
                const response = await fetch('http://localhost:5000/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                if (data.message) {
                    document.getElementById('recording-status').textContent = data.message;
                    document.getElementById('text-output').textContent = data.text;
                    document.getElementById('notes-output').textContent = data.summary;
                } else if (data.error) {
                    document.getElementById('recording-status').textContent = 'Error: ' + data.error;
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('An error occurred: ' + error.message);
            }
        };

        mediaRecorder.start();
    } catch (error) {
        console.error('Recording error:', error);
        alert('Could not start recording: ' + error.message);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        stopTimer();
        document.getElementById('recording-status').innerHTML = 'Ready to record...';
        document.getElementById('recording-dot').style.display = 'none';
    }
}

function startTimer() {
    timerInterval = setInterval(() => {
        const now = new Date();
        elapsedRecordingTime = now - startTime;
        const elapsedTime = new Date(elapsedRecordingTime);
        const hours = String(elapsedTime.getUTCHours()).padStart(2, '0');
        const minutes = String(elapsedTime.getUTCMinutes()).padStart(2, '0');
        const seconds = String(elapsedTime.getUTCSeconds()).padStart(2, '0');
        document.getElementById('time-elapsed').textContent = `${hours}:${minutes}:${seconds}`;
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}
