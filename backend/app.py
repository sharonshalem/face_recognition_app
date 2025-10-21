from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import numpy as np
from face_service import FaceRecognitionService
from rembg import remove

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize face recognition service
face_service = FaceRecognitionService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "face-recognition-api"})

@app.route('/recognize', methods=['POST'])
def recognize_face():
    """
    Endpoint to recognize faces in an image
    Expects JSON with base64 encoded image
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to numpy array (RGB)
        image_array = np.array(image)
        
        # Perform face recognition
        results = face_service.recognize_faces(image_array)
        
        return jsonify({
            "success": True,
            "faces_detected": len(results),
            "results": results
        })
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/known-faces', methods=['GET'])
def get_known_faces():
    """Get list of known faces"""
    try:
        known_faces = face_service.get_known_faces_list()
        return jsonify({
            "success": True,
            "known_faces": known_faces
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove-background', methods=['POST'])
def remove_background():
    """
    Endpoint to remove background from an image and replace with selected color
    Expects JSON with base64 encoded image and background color (hex format)
    """
    try:
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({"error": "No image provided"}), 400

        # Get background color (default to white if not provided)
        bg_color = data.get('backgroundColor', '#FFFFFF')

        # Convert hex color to RGB tuple
        bg_color = bg_color.lstrip('#')
        bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))

        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)

        # Convert to PIL Image
        input_image = Image.open(io.BytesIO(image_bytes))

        # Remove background (returns image with transparent background)
        output_image = remove(input_image)

        # Create a new image with the selected background color
        if output_image.mode == 'RGBA':
            # Create background with selected color
            background = Image.new('RGB', output_image.size, bg_rgb)
            # Paste the image with transparency onto the colored background
            background.paste(output_image, mask=output_image.split()[3])
            output_image = background

        # Convert to base64
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            "success": True,
            "image": f"data:image/png;base64,{img_str}",
            "backgroundColor": data.get('backgroundColor', '#FFFFFF')
        })

    except Exception as e:
        print(f"Error removing background: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Face Recognition API...")
    print("Loading known faces...")
    face_service.load_known_faces()
    print(f"Loaded {len(face_service.known_face_names)} known faces")
    print("API running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)