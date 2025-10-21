from PIL import Image
import os

def convert_to_rgb(image_path):
    """Convert image to proper RGB format for face_recognition"""
    try:
        img = Image.open(image_path)
        print(f"Image: {os.path.basename(image_path)}")
        print(f"  Mode: {img.mode}, Size: {img.size}, Format: {img.format}")
        
        # Always convert to RGB and resave to ensure compatibility
        # This removes alpha channels, ensures 8-bit depth, etc.
        rgb_img = img.convert('RGB')
        
        # Save with explicit JPEG format for maximum compatibility
        base_name = os.path.splitext(image_path)[0]
        new_path = base_name + '_fixed.jpg'
        rgb_img.save(new_path, 'JPEG', quality=95)
        
        # Remove old file and rename new one
        os.remove(image_path)
        os.rename(new_path, image_path)
        
        print(f"✓ Fixed and saved {os.path.basename(image_path)}")
            
    except Exception as e:
        print(f"✗ Error with {os.path.basename(image_path)}: {e}")

def main():
    known_faces_dir = 'known_faces'
    
    if not os.path.exists(known_faces_dir):
        print(f"Directory {known_faces_dir} not found!")
        return
    
    print("Converting images to RGB format...")
    print("-" * 50)
    
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    for filename in os.listdir(known_faces_dir):
        name, ext = os.path.splitext(filename)
        
        if ext.lower() in valid_extensions:
            image_path = os.path.join(known_faces_dir, filename)
            convert_to_rgb(image_path)
    
    print("-" * 50)
    print("Done! Now restart your app with: py -3.12 app.py")

if __name__ == '__main__':
    main()