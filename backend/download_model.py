"""
Temporary script to download rembg model with SSL verification disabled
This is needed for corporate networks that intercept HTTPS traffic
"""
import ssl
import warnings

# Disable SSL verification warnings
warnings.filterwarnings('ignore')

# Create unverified SSL context (only for this download)
ssl._create_default_https_context = ssl._create_unverified_context

print("Downloading rembg AI model (u2net.onnx - ~176MB)...")
print("This may take a few minutes depending on your connection...")

try:
    from rembg import remove
    from PIL import Image
    import io

    # Create a small test image to trigger model download
    test_img = Image.new('RGB', (100, 100), color='red')

    print("Triggering model download...")
    result = remove(test_img)

    print("\n✓ Model downloaded successfully!")
    print("You can now use the background removal feature.")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nIf this fails, you may need to:")
    print("1. Download the model manually from a browser")
    print("2. Contact your IT department about SSL inspection")
