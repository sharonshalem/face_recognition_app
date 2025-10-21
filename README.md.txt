# Face Recognition App

A real-time face recognition system with a web frontend and Flask backend API.

## Features

- 📷 Real-time camera access
- 🎯 Face detection and recognition
- 🔍 Confidence scoring
- 📊 Multiple face detection
- 🌐 Clean web interface

## Project Structure

```
face_recognition_app/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── face_service.py           # Face recognition logic
│   └── known_faces/              # Store reference images here
│       ├── john.jpg
│       ├── jane.jpg
│       └── ...
├── frontend/
│   ├── index.html                # Web interface
│   ├── style.css                 # Styling
│   └── app.js                    # Frontend logic
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions

### 1. Install Dependencies

Make sure you already have Python 3.12 installed with dlib, face-recognition, and opencv-python.

Install Flask and other requirements:

```cmd
cd C:\Users\sharon_shalem\git\face_recognition_app
pip install -r requirements.txt
```

### 2. Add Known Faces

Add reference images to the `backend/known_faces/` folder:

- Images should be `.jpg`, `.jpeg`, or `.png`
- Each image should contain ONE clear face
- Name the file as the person's name (e.g., `john_doe.jpg`)
- The file name becomes the recognized name (without extension)

Example:
```
backend/known_faces/
├── alice.jpg
├── bob.jpg
└── charlie.jpg
```

### 3. Start the Backend Server

```cmd
cd backend
python app.py
```

You should see:
```
Starting Face Recognition API...
Loading known faces...
✓ Loaded: alice
✓ Loaded: bob
✓ Loaded: charlie
Total known faces loaded: 3
API running on http://localhost:5000
```

### 4. Open the Frontend

Open `frontend/index.html` in your web browser:

**Option 1:** Double-click the file

**Option 2:** Right-click → Open with → Chrome/Firefox

**Option 3:** Use VSCode Live Server extension

### 5. Use the App

1. Click "Start Camera" to enable your webcam
2. Position faces in front of the camera
3. Click "Capture & Recognize" to identify faces
4. See results with names and confidence scores!

## API Endpoints

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "face-recognition-api"
}
```

### POST /recognize
Recognize faces in an image

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

**Response:**
```json
{
  "success": true,
  "faces_detected": 2,
  "results": [
    {
      "name": "alice",
      "confidence": 0.89,
      "location": {
        "top": 100,
        "right": 300,
        "bottom": 250,
        "left": 150
      }
    }
  ]
}
```

### GET /known-faces
Get list of loaded known faces

**Response:**
```json
{
  "success": true,
  "known_faces": ["alice", "bob", "charlie"]
}
```

## Troubleshooting

### Camera Not Working
- Allow browser camera permissions when prompted
- Make sure no other app is using the camera
- Try refreshing the page

### Backend Connection Error
- Verify the backend is running on port 5000
- Check console for error messages
- Make sure Flask server shows "Running on http://localhost:5000"

### No Faces Detected
- Ensure good lighting
- Face the camera directly
- Move closer to the camera
- Make sure face is clearly visible

### Unknown Face
- Add reference image to `backend/known_faces/`
- Restart the backend server
- Use clear, well-lit reference photos

## Technologies Used

- **Backend:** Flask, face_recognition, OpenCV, dlib
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **API:** RESTful API with JSON

## Tips for Best Results

1. **Good lighting** - Face should be well-lit
2. **Clear images** - Use high-quality reference photos
3. **Front-facing** - Face should face the camera directly
4. **Single face** - Each reference image should have one face
5. **Multiple angles** - Add multiple images of same person for better accuracy

## License

MIT License - Feel free to use and modify!