# Face Recognition & Background Removal App

A full-stack web application that provides face recognition and AI-powered background removal capabilities.

## Features

- **Face Recognition**: Real-time face detection and recognition using webcam
- **Background Removal**: AI-powered background removal with custom color replacement
- **Easy Face Management**: Add known faces by simply placing images in a folder
- **Modern UI**: Clean, responsive interface built with HTML/CSS/JavaScript
- **RESTful API**: Flask-based backend with well-documented endpoints

## Tech Stack

### Backend
- Python 3.12
- Flask (Web Framework)
- face-recognition (Face detection and recognition)
- rembg (AI background removal)
- OpenCV (Image processing)
- dlib (Face detection models)

### Frontend
- HTML5/CSS3
- Vanilla JavaScript
- Nginx (for production deployment)

### Deployment
- Docker & Docker Compose
- Ready for AWS, GCP, Azure, or any cloud platform

## Project Structure

```
face_recognition_app/
├── backend/
│   ├── app.py                 # Flask application
│   ├── face_service.py        # Face recognition logic
│   ├── known_faces/           # Directory for known face images
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend container configuration
├── frontend/
│   ├── index.html            # Main HTML page
│   ├── app.js                # Frontend JavaScript
│   ├── style.css             # Styling
│   ├── nginx.conf            # Nginx configuration
│   └── Dockerfile            # Frontend container configuration
├── docker-compose.yml        # Multi-container orchestration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (for containerized deployment)
- Webcam (for face recognition feature)

### Local Development Setup

#### 1. Clone the repository

```bash
git clone <your-repo-url>
cd face_recognition_app
```

#### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
pip install rembg onnxruntime
```

#### 3. Add Known Faces

Create the `backend/known_faces/` directory and add face images:
- File format: JPG, JPEG, or PNG
- File naming: `PersonName.jpg` (the filename becomes the person's name)
- Example: `sharon.jpg`, `john_doe.png`

#### 4. Run Backend

```bash
cd backend
python app.py
```

Backend will be available at `http://localhost:5000`

#### 5. Run Frontend

```bash
cd frontend
python -m http.server 8000
```

Frontend will be available at `http://localhost:8000`

### Docker Deployment

#### Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will start both frontend and backend containers:
- Frontend: `http://localhost:8000`
- Backend: `http://localhost:5000`

#### Stop Containers

```bash
docker-compose down
```

## API Endpoints

### Health Check
```
GET /health
```
Returns API health status.

### Recognize Faces
```
POST /recognize
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,<base64-encoded-image>"
}
```

Returns detected faces with names and confidence scores.

### Get Known Faces
```
GET /known-faces
```

Returns list of all known face names.

### Remove Background
```
POST /remove-background
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,<base64-encoded-image>",
  "backgroundColor": "#FFFFFF"
}
```

Returns image with background removed and replaced with specified color.

## Usage

### Face Recognition

1. Open the app in your browser
2. Click "Start Camera" to activate your webcam
3. Position your face in front of the camera
4. Click "Capture & Recognize" to identify faces
5. Results will show matched names with confidence levels

### Background Removal

1. Scroll to the "Background Removal" section
2. Click "Upload Image" to select a photo
3. Choose your desired background color using the color picker
4. Click "Remove Background" to process
5. Download the processed image

## Cloud Deployment

### AWS Deployment Options

#### Option 1: AWS Elastic Beanstalk
1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create`
4. Deploy: `eb deploy`

#### Option 2: AWS ECS (Elastic Container Service)
1. Build and push Docker images to ECR
2. Create ECS cluster
3. Define task definitions
4. Create services

#### Option 3: AWS EC2
1. Launch EC2 instance
2. Install Docker
3. Clone repository
4. Run with docker-compose

### Other Cloud Platforms

**Railway.app** (Recommended for simplicity)
1. Connect GitHub repository
2. Auto-detects Dockerfile
3. Deploys automatically

**Heroku**
1. Create `Procfile`
2. `heroku create`
3. `git push heroku main`

**Google Cloud Run**
1. Build container: `gcloud builds submit`
2. Deploy: `gcloud run deploy`

## Configuration

### Environment Variables

Backend (`backend/.env`):
```
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000
```

### Model Files

The background removal feature requires downloading the `u2net.onnx` model (~176MB):
- URL: https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
- Location: `C:\Users\<username>\.u2net\u2net.onnx` (Windows)
- Location: `~/.u2net/u2net.onnx` (Linux/Mac)

For Docker deployments, the model is cached in a Docker volume.

## Troubleshooting

### SSL Certificate Errors (Corporate Networks)

If you encounter SSL certificate errors when downloading the model:
1. Download the model manually from the URL above
2. Place it in the `.u2net` directory
3. Restart the application

### Camera Access Issues

- Ensure HTTPS is used (required for camera access in browsers)
- Check browser permissions
- For local development, localhost is allowed

### Known Faces Not Loading

- Verify images are in `backend/known_faces/` directory
- Check file extensions (.jpg, .jpeg, .png)
- Ensure at least one face is visible in each image
- Check backend logs for errors

## Development

### Adding New Features

1. Create a new branch: `git checkout -b feature-name`
2. Make changes
3. Test locally
4. Commit: `git commit -m "Description"`
5. Push: `git push origin feature-name`
6. Create Pull Request

### Running Tests

```bash
cd backend
pytest
```

## Security Considerations

- Do not commit known face images to version control
- Use environment variables for sensitive configuration
- Implement authentication for production deployments
- Use HTTPS in production
- Rate limit API endpoints

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Authors

Sharon Shalem

## Acknowledgments

- face_recognition library by Adam Geitgey
- rembg library by Daniel Gatis
- Flask framework
- OpenCV community
