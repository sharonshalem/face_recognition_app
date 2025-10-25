"""
Simple background removal using OpenCV - no AI models required!
Uses GrabCut algorithm for intelligent foreground/background segmentation
"""
import cv2
import numpy as np
from PIL import Image


def remove_background_simple(image, bg_color=(255, 255, 255)):
    """
    Remove background using OpenCV's GrabCut algorithm

    Args:
        image: PIL Image or numpy array
        bg_color: RGB tuple for background color (default white)

    Returns:
        PIL Image with background replaced by bg_color
    """
    # Convert PIL to numpy if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image

    # Ensure RGB format
    if len(img_array.shape) == 2:  # Grayscale
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

    # Create mask
    mask = np.zeros(img_array.shape[:2], np.uint8)

    # Create temporary arrays for GrabCut
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Define rectangle around the subject (slightly inside the image borders)
    height, width = img_array.shape[:2]
    margin = min(width, height) // 20  # 5% margin
    rect = (margin, margin, width - margin * 2, height - margin * 2)

    # Apply GrabCut algorithm
    # This assumes the subject is roughly in the center
    try:
        cv2.grabCut(img_array, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

        # Create binary mask where 0 and 2 are background, 1 and 3 are foreground
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Apply morphological operations to smooth the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)

        # Optional: blur the mask edges for smoother transition
        mask2 = cv2.GaussianBlur(mask2, (5, 5), 0)

        # Create output image with custom background
        output = np.full_like(img_array, bg_color, dtype=np.uint8)

        # Blend foreground with new background
        for c in range(3):
            output[:, :, c] = output[:, :, c] * (1 - mask2) + img_array[:, :, c] * mask2

        # Convert back to PIL Image
        return Image.fromarray(output)

    except Exception as e:
        print(f"GrabCut failed: {e}")
        # Fallback: return original image with note
        return Image.fromarray(img_array)


def remove_background_edge_detection(image, bg_color=(255, 255, 255)):
    """
    Alternative method using edge detection and flood fill
    Works better for images with clear subject boundaries
    """
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image

    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Dilate edges to close gaps
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=2)

    # Create mask using flood fill from corners (assumes background is at corners)
    height, width = edges.shape
    mask = np.zeros((height + 2, width + 2), np.uint8)

    # Flood fill from all four corners
    cv2.floodFill(edges, mask, (0, 0), 255)
    cv2.floodFill(edges, mask, (width - 1, 0), 255)
    cv2.floodFill(edges, mask, (0, height - 1), 255)
    cv2.floodFill(edges, mask, (width - 1, height - 1), 255)

    # Invert mask
    mask = mask[1:-1, 1:-1]
    mask = cv2.bitwise_not(mask)

    # Apply to original image
    output = np.full_like(img_array, bg_color, dtype=np.uint8)
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) / 255.0
    output = (output * (1 - mask_3ch) + img_array * mask_3ch).astype(np.uint8)

    return Image.fromarray(output)
