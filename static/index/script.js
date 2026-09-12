document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Live Webcam Feed
    const videoElement = document.getElementById('cameraFeed');

    async function initCamera() {
        try {
            const constraints = {
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: "user" 
                },
                audio: false
            };
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            videoElement.srcObject = stream;
        } catch (error) {
            console.error("Camera access denied or unavailable:", error);
            alert("Could not access the camera. Please ensure permissions are granted and you are running via localhost or HTTPS.");
        }
    }

    initCamera();

    // 2. Shutter Button Capture & Server Upload Effect
    const shutterBtn = document.getElementById('shutterBtn');
    
    shutterBtn.addEventListener('click', () => {
        const viewfinder = document.querySelector('.viewfinder');
        viewfinder.style.opacity = '0.2';
        
        setTimeout(() => {
            viewfinder.style.opacity = '1';

            // Create a temporary canvas to capture the current frame
            const canvas = document.createElement('canvas');
            canvas.width = videoElement.videoWidth || 1280;
            canvas.height = videoElement.videoHeight || 720;
            const ctx = canvas.getContext('2d');
            
            // Draw video frame onto canvas
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

            // Convert canvas into a Base64 string image format
            const base64Image = canvas.toDataURL('image/png');

            // Send image payload to FastAPI server endpoint
            fetch('/api/save-photo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64Image })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                alert('Photo captured and saved to server root under /saved_photos/capture.png!');
            })
            .catch(error => {
                console.error('Error saving photo:', error);
                alert('Failed to save photo to server.');
            });

        }, 150);
    });
});