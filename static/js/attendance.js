// Update current time
function updateCurrentTime() {
    const timeElement = document.getElementById('current-time');
    const now = new Date();
    timeElement.textContent = now.toLocaleTimeString();
}

// Update attendance status
function updateAttendanceStatus() {
    fetch('/api/attendance-status')
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById('attendance-status');
            if (data.status) {
                statusElement.innerHTML = `
                    <span class="badge bg-${data.status.toLowerCase()}">
                        ${data.status}
                    </span>
                `;
            }
        })
        .catch(error => console.error('Error fetching attendance status:', error));
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Update time every second
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    // Update attendance status every minute
    updateAttendanceStatus();
    setInterval(updateAttendanceStatus, 60000);
});
