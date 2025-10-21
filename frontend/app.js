// API Configuration
// Use environment variable or default to localhost
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : `http://${window.location.hostname}:5000`;

// DOM Elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startCameraBtn = document.getElementById('startCamera');
const captureBtn = document.getElementById('captureBtn');
const stopCameraBtn = document.getElementById('stopCamera');
const statusDiv = document.getElementById('status');
const resultsDiv = document.getElementById('results');
const knownFacesDiv = document.getElementById('knownFaces');

// Background Removal Elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const removeBgBtn = document.getElementById('removeBgBtn');
const colorPicker = document.getElementById('colorPicker');
const colorValue = document.getElementById('colorValue');
const originalImage = document.getElementById('originalImage');
const processedImage = document.getElementById('processedImage');
const originalPlaceholder = document.getElementById('originalPlaceholder');
const processedPlaceholder = document.getElementById('processedPlaceholder');
const bgStatus = document.getElementById('bgStatus');
const downloadBtn = document.getElementById('downloadBtn');

let stream = null;
let uploadedImageData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadKnownFaces();

    // Event Listeners - Face Recognition
    startCameraBtn.addEventListener('click', startCamera);
    captureBtn.addEventListener('click', captureAndRecognize);
    stopCameraBtn.addEventListener('click', stopCamera);

    // Event Listeners - Background Removal
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
    removeBgBtn.addEventListener('click', removeBackgroundFromImage);
    colorPicker.addEventListener('input', updateColorValue);
    downloadBtn.addEventListener('click', downloadProcessedImage);
});

// Load known faces from API
async function loadKnownFaces() {
    try {
        const response = await fetch(`${API_URL}/known-faces`);
        const data = await response.json();
        
        if (data.success && data.known_faces.length > 0) {
            knownFacesDiv.innerHTML = data.known_faces
                .map(name => `<span class="face-tag">${name}</span>`)
                .join('');
        } else {
            knownFacesDiv.innerHTML = '<p class="loading">No known faces loaded yet. Add images to backend/known_faces/</p>';
        }
    } catch (error) {
        console.error('Error loading known faces:', error);
        knownFacesDiv.innerHTML = '<p class="loading">Error loading known faces</p>';
    }
}

// Start camera
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        
        // Update UI
        startCameraBtn.disabled = true;
        captureBtn.disabled = false;
        stopCameraBtn.disabled = false;
        
        updateStatus('Camera started successfully', 'success');
    } catch (error) {
        console.error('Error accessing camera:', error);
        updateStatus('Error: Could not access camera. Please check permissions.', 'error');
    }
}

// Stop camera
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        stream = null;
    }
    
    // Update UI
    startCameraBtn.disabled = false;
    captureBtn.disabled = true;
    stopCameraBtn.disabled = true;
    
    updateStatus('Camera stopped', 'success');
}

// Capture image and send to API
async function captureAndRecognize() {
    try {
        updateStatus('Capturing and processing...', 'processing');
        
        // Set canvas dimensions to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw current video frame to canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert canvas to base64
        const imageData = canvas.toDataURL('image/jpeg');
        
        // Send to API
        const response = await fetch(`${API_URL}/recognize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            updateStatus('Error: ' + (data.error || 'Unknown error'), 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        updateStatus('Error: Could not connect to recognition service. Make sure backend is running on port 5000.', 'error');
    }
}

// Display recognition results
function displayResults(data) {
    if (data.faces_detected === 0) {
        updateStatus('No faces detected in the image', 'error');
        resultsDiv.innerHTML = '<p style="color: #718096;">No faces found. Try again with better lighting or positioning.</p>';
        return;
    }
    
    updateStatus(`Found ${data.faces_detected} face(s)!`, 'success');
    
    resultsDiv.innerHTML = data.results.map((face, index) => {
        const isKnown = face.name !== 'Unknown';
        const confidencePercent = (face.confidence * 100).toFixed(1);
        
        return `
            <div class="face-result ${!isKnown ? 'unknown' : ''}">
                <h3>Face ${index + 1}: ${face.name}</h3>
                ${isKnown ? `<p><span class="confidence">${confidencePercent}% confident</span></p>` : ''}
                <p>Location: Top: ${face.location.top}, Left: ${face.location.left}</p>
            </div>
        `;
    }).join('');
}

// Update status message
function updateStatus(message, type = '') {
    statusDiv.textContent = message;
    statusDiv.className = 'status ' + type;
}

// Background Removal Functions

function updateColorValue() {
    colorValue.textContent = colorPicker.value.toUpperCase();
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImageData = e.target.result;

        // Show original image
        originalImage.src = uploadedImageData;
        originalImage.style.display = 'block';
        originalPlaceholder.style.display = 'none';

        // Enable remove background button
        removeBgBtn.disabled = false;

        // Reset processed image
        processedImage.style.display = 'none';
        processedPlaceholder.style.display = 'block';
        downloadBtn.style.display = 'none';

        updateBgStatus('Image uploaded successfully! Choose a color and click "Remove Background"', 'success');
    };

    reader.readAsDataURL(file);
}

async function removeBackgroundFromImage() {
    if (!uploadedImageData) {
        updateBgStatus('Please upload an image first', 'error');
        return;
    }

    try {
        updateBgStatus('Processing... This may take a few seconds', 'processing');
        removeBgBtn.disabled = true;

        const response = await fetch(`${API_URL}/remove-background`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: uploadedImageData,
                backgroundColor: colorPicker.value
            })
        });

        const data = await response.json();

        if (data.success) {
            // Show processed image
            processedImage.src = data.image;
            processedImage.style.display = 'block';
            processedPlaceholder.style.display = 'none';
            downloadBtn.style.display = 'block';

            updateBgStatus('Background removed successfully!', 'success');
        } else {
            updateBgStatus('Error: ' + (data.error || 'Unknown error'), 'error');
        }

    } catch (error) {
        console.error('Error:', error);
        updateBgStatus('Error: Could not connect to background removal service. Make sure backend is running.', 'error');
    } finally {
        removeBgBtn.disabled = false;
    }
}

function downloadProcessedImage() {
    if (!processedImage.src) return;

    const link = document.createElement('a');
    link.href = processedImage.src;
    link.download = `background-removed-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    updateBgStatus('Image downloaded!', 'success');
}

function updateBgStatus(message, type = '') {
    bgStatus.textContent = message;
    bgStatus.className = 'status ' + type;
}