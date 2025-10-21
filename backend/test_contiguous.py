import cv2
import numpy as np
import face_recognition
import os

def test_with_contiguous(image_path):
    print(f"\nTesting: {os.path.basename(image_path)}")
    print("-" * 50)
    
    # Load with OpenCV
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    print(f"Original array:")
    print(f"  Shape: {img_rgb.shape}, Dtype: {img_rgb.dtype}")
    print(f"  Contiguous: {img_rgb.flags['C_CONTIGUOUS']}")
    print(f"  Writable: {img_rgb.flags['WRITEABLE']}")
    
    # Ensure contiguous and writable
    img_contiguous = np.ascontiguousarray(img_rgb, dtype=np.uint8)
    
    print(f"\nContiguous array:")
    print(f"  Shape: {img_contiguous.shape}, Dtype: {img_contiguous.dtype}")
    print(f"  Contiguous: {img_contiguous.flags['C_CONTIGUOUS']}")
    print(f"  Writable: {img_contiguous.flags['WRITEABLE']}")
    
    # Try face detection
    try:
        print("\nAttempting face detection...")
        encodings = face_recognition.face_encodings(img_contiguous)
        print(f"✓ SUCCESS! Found {len(encodings)} face(s)")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    known_faces_dir = 'known_faces'
    
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    for filename in os.listdir(known_faces_dir):
        name, ext = os.path.splitext(filename)
        if ext.lower() in valid_extensions:
            image_path = os.path.join(known_faces_dir, filename)
            test_with_contiguous(image_path)

if __name__ == '__main__':
    main()