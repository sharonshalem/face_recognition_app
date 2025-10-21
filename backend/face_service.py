import face_recognition
import os
import numpy as np
import cv2

class FaceRecognitionService:
    def __init__(self, known_faces_dir='known_faces'):
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        
    def load_known_faces(self):
        """Load all known faces from the known_faces directory"""
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            print(f"Created directory: {self.known_faces_dir}")
            print("Please add face images to this directory!")
            return
        
        valid_extensions = ['.jpg', '.jpeg', '.png']
        
        for filename in os.listdir(self.known_faces_dir):
            name, ext = os.path.splitext(filename)
            
            if ext.lower() in valid_extensions:
                image_path = os.path.join(self.known_faces_dir, filename)
                
                try:
                    # Load image using OpenCV (more reliable)
                    image = cv2.imread(image_path)
                    
                    if image is None:
                        print(f"[X] Could not load image: {filename}")
                        continue
                    
                    # Convert BGR to RGB (OpenCV uses BGR by default)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Get face encodings
                    encodings = face_recognition.face_encodings(image)
                    
                    if len(encodings) > 0:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(name)
                        print(f"[OK] Loaded: {name}")
                    else:
                        print(f"[X] No face found in: {filename}")
                        
                except Exception as e:
                    print(f"[X] Error loading {filename}: {str(e)}")
        
        print(f"\nTotal known faces loaded: {len(self.known_face_names)}")
    
    def recognize_faces(self, image_array):
        """
        Recognize faces in the given image
        Returns list of dictionaries with face locations and names
        """
        results = []
        
        # Find all face locations and encodings in the image
        face_locations = face_recognition.face_locations(image_array)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        # Loop through each face found
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            confidence = 0.0
            
            if len(self.known_face_encodings) > 0:
                # Compare face with known faces
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, 
                    face_encoding,
                    tolerance=0.6
                )
                
                # Calculate face distances
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, 
                    face_encoding
                )
                
                # Find best match
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
            
            results.append({
                "name": name,
                "confidence": float(confidence),
                "location": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left
                }
            })
        
        return results
    
    def get_known_faces_list(self):
        """Return list of known face names"""
        return self.known_face_names