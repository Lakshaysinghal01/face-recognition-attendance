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
        video.style.display = 'block';
        canvas.style.display = 'none';
        captureBtn.style.display = 'block';
        retakeBtn.style.display = 'none';
    } catch (err) {
        showError('Failed to access webcam: ' + err.message);
    }
}

// Capture photo
async function capturePhoto() {
    try {
        canvas.style.display = 'block';
        video.style.display = 'none';
        captureBtn.style.display = 'none';
        retakeBtn.style.display = 'block';

        // Set canvas dimensions to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw video frame to canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // Convert canvas to blob
        const blob = await new Promise(resolve => {
            canvas.toBlob(resolve, 'image/jpeg', 0.8);
        });

        if (!blob) {
            throw new Error('Failed to create image blob');
        }

        // Create form data
        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');

        // Show processing status
        showInfo('Processing...');

        // Send to server
        const response = await fetch('/api/mark-attendance', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showSuccess(data.message);
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showError(data.message || 'Failed to mark attendance');
            retakePhoto();
        }
    } catch (error) {
        showError('Error: ' + error.message);
        retakePhoto();
    }
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

function showInfo(message) {
    statusContainer.innerHTML = `
        <div class="alert alert-info">
            <i data-feather="info"></i> ${message}
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