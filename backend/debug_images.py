import cv2
import numpy as np
from PIL import Image
import face_recognition
import os

def debug_image(image_path):
    print(f"\n{'='*60}")
    print(f"Debugging: {os.path.basename(image_path)}")
    print('='*60)
    
    # Check with PIL
    print("\n1. PIL Analysis:")
    try:
        pil_img = Image.open(image_path)
        print(f"   Mode: {pil_img.mode}")
        print(f"   Size: {pil_img.size}")
        print(f"   Format: {pil_img.format}")
        print(f"   Bits: {pil_img.bits if hasattr(pil_img, 'bits') else 'N/A'}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Check with OpenCV
    print("\n2. OpenCV Analysis:")
    try:
        cv_img = cv2.imread(image_path)
        if cv_img is not None:
            print(f"   Shape: {cv_img.shape}")
            print(f"   Dtype: {cv_img.dtype}")
            print(f"   Min/Max: {cv_img.min()}/{cv_img.max()}")
            
            # Convert to RGB
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            print(f"   RGB Shape: {rgb_img.shape}")
            print(f"   RGB Dtype: {rgb_img.dtype}")
        else:
            print("   Could not load with OpenCV")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Try face_recognition.load_image_file
    print("\n3. face_recognition.load_image_file:")
    try:
        fr_img = face_recognition.load_image_file(image_path)
        print(f"   Shape: {fr_img.shape}")
        print(f"   Dtype: {fr_img.dtype}")
        print(f"   Min/Max: {fr_img.min()}/{fr_img.max()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Try to detect faces
    print("\n4. Face Detection Test:")
    try:
        # Method 1: Using face_recognition.load_image_file
        print("   Method 1 (face_recognition.load_image_file):")
        img1 = face_recognition.load_image_file(image_path)
        encodings1 = face_recognition.face_encodings(img1)
        print(f"   ✓ Found {len(encodings1)} face(s)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Method 2: Using OpenCV
        print("   Method 2 (OpenCV + convert to RGB):")
        img2 = cv2.imread(image_path)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        encodings2 = face_recognition.face_encodings(img2)
        print(f"   ✓ Found {len(encodings2)} face(s)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Method 3: Using PIL
        print("   Method 3 (PIL + convert):")
        img3 = Image.open(image_path).convert('RGB')
        img3_array = np.array(img3)
        print(f"   Array shape: {img3_array.shape}, dtype: {img3_array.dtype}")
        encodings3 = face_recognition.face_encodings(img3_array)
        print(f"   ✓ Found {len(encodings3)} face(s)")
    except Exception as e:
        print(f"   ✗ Error: {e}")

def main():
    known_faces_dir = 'known_faces'
    
    if not os.path.exists(known_faces_dir):
        print(f"Directory {known_faces_dir} not found!")
        return
    
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    for filename in os.listdir(known_faces_dir):
        name, ext = os.path.splitext(filename)
        if ext.lower() in valid_extensions:
            image_path = os.path.join(known_faces_dir, filename)
            debug_image(image_path)

if __name__ == '__main__':
    main()