document.getElementById('start-recording').addEventListener('click', startRecording);
document.getElementById('stop-recording').addEventListener('click', stopRecording);

function startRecording() {
    document.getElementById('recording-status').innerHTML = '<span id="recording-dot"></span> Recording...';
    document.getElementById('recording-dot').style.display = 'inline-block';
    // 여기서 녹음을 시작하는 코드를 추가할 수 있습니다.
}

function stopRecording() {
    document.getElementById('recording-status').innerHTML = 'Ready to record...';
    document.getElementById('recording-dot').style.display = 'none';
    // 여기서 녹음을 멈추고 텍스트 변환 코드를 추가할 수 있습니다.
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Success: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred');
    });
}

// http를 통해서 파일을 주고 받는 것을 구현