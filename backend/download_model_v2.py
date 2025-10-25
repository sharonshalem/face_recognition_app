"""
Download rembg model by patching requests library to bypass SSL
"""
import os
import ssl
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set environment variable to disable SSL verification
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

# Monkey patch requests to disable SSL verification
import requests
from functools import partialmethod
requests.Session.request = partialmethod(requests.Session.request, verify=False)

# Disable SSL verification in urllib3
ssl._create_default_https_context = ssl._create_unverified_context

print("Downloading rembg AI model (u2net.onnx - ~176MB)...")
print("This may take a few minutes depending on your connection...")
print("SSL verification is disabled for this download (corporate network workaround)")

try:
    from rembg import remove
    from PIL import Image

    # Create a small test image to trigger model download
    test_img = Image.new('RGB', (100, 100), color='red')

    print("\nTriggering model download...")
    result = remove(test_img)

    print("\n[OK] Model downloaded successfully!")
    print("Model location: C:\\Users\\sharon_shalem\\.u2net\\u2net.onnx")
    print("\nYou can now use the background removal feature.")
    print("The backend will need to be restarted if it's already running.")

except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    print("\nIf this fails, you may need to:")
    print("1. Download manually: https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx")
    print("2. Save it to: C:\\Users\\sharon_shalem\\.u2net\\u2net.onnx")
    print("3. Contact your IT department about SSL inspection")
