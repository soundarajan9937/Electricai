import cv2
import os


def is_meter_image(image_path):
    """
    Basic image validation.

    YOLO detection is handled separately in meter_detection.py.
    This function does NOT load YOLO, which saves RAM.
    """

    print("Checking uploaded image...")

    if not os.path.exists(image_path):
        print("Image does not exist:", image_path)
        return False

    image = cv2.imread(image_path)

    if image is None:
        print("Unable to read image.")
        return False

    # Make sure the image has reasonable dimensions
    height, width = image.shape[:2]

    print("Image size:", width, "x", height)

    if width < 50 or height < 50:
        print("Image is too small.")
        return False

    print("Image validation successful.")
    return True