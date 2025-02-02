let video = document.getElementById('webcam');
let canvas = document.getElementById('preview');
let captureBtn = document.getElementById('capture-btn');
let retakeBtn = document.getElementById('retake-btn');
let statusContainer = document.getElementById('status-container');
let stream = null;

// Initialize webcam
async function initWebcam() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: "user"
            }
        });
        video.srcObject = stream;
    } catch (err) {
        showError('Failed to access webcam: ' + err.message);
    }
}

// Capture photo
function capturePhoto() {
    canvas.style.display = 'block';
    video.style.display = 'none';
    captureBtn.style.display = 'none';
    retakeBtn.style.display = 'block';
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    // Convert to blob and send to server
    canvas.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');
        
        fetch('/api/mark-attendance', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccess('Attendance marked successfully!');
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                showError(data.message || 'Failed to mark attendance');
            }
        })
        .catch(error => {
            showError('Error: ' + error.message);
        });
    }, 'image/jpeg', 0.8);
}

// Retake photo
function retakePhoto() {
    canvas.style.display = 'none';
    video.style.display = 'block';
    captureBtn.style.display = 'block';
    retakeBtn.style.display = 'none';
}

// Status display functions
function showSuccess(message) {
    statusContainer.innerHTML = `
        <div class="alert alert-success">
            <i data-feather="check-circle"></i> ${message}
        </div>
    `;
    feather.replace();
}

function showError(message) {
    statusContainer.innerHTML = `
        <div class="alert alert-danger">
            <i data-feather="alert-circle"></i> ${message}
        </div>
    `;
    feather.replace();
}

// Event listeners
document.addEventListener('DOMContentLoaded', initWebcam);
captureBtn.addEventListener('click', capturePhoto);
retakeBtn.addEventListener('click', retakePhoto);

// Cleanup
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
