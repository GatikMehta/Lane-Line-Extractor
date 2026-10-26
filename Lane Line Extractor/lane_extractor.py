"""Classical CV lane line extractor.

Pipeline: load -> HSV colour mask -> Gaussian blur -> Canny -> ROI mask.
Usage:  python lane_extractor.py images/road1.jpg [more images...]
Outputs are saved to ./output/<name>_*.jpg
"""
import os
import sys

import cv2
import numpy as np

# HSV ranges (OpenCV: H 0-179, S 0-255, V 0-255). Tune for your images.
WHITE_LOW, WHITE_HIGH = np.array([0, 0, 200]), np.array([180, 40, 255])
YELLOW_LOW, YELLOW_HIGH = np.array([15, 80, 120]), np.array([35, 255, 255])


def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img


def color_filter(img):
    """Keep only white and yellow pixels (typical lane paint) using HSV."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(hsv, WHITE_LOW, WHITE_HIGH)
    yellow = cv2.inRange(hsv, YELLOW_LOW, YELLOW_HIGH)
    mask = cv2.bitwise_or(white, yellow)
    return mask, cv2.bitwise_and(img, img, mask=mask)


def blur(gray_or_img, k=5):
    return cv2.GaussianBlur(gray_or_img, (k, k), 0)


def detect_edges(img, low=50, high=150):
    return cv2.Canny(img, low, high)


def region_of_interest(edges):
    """Mask everything outside a trapezoid covering the road ahead."""
    h, w = edges.shape[:2]
    polygon = np.array([[
        (int(0.05 * w), h),
        (int(0.45 * w), int(0.60 * h)),
        (int(0.55 * w), int(0.60 * h)),
        (int(0.95 * w), h),
    ]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(edges, mask), polygon


def process(path, out_dir="output"):
    os.makedirs(out_dir, exist_ok=True)
    name = os.path.splitext(os.path.basename(path))[0]

    img = load_image(path)
    mask, filtered = color_filter(img)
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    blurred = blur(gray)
    edges = detect_edges(blurred)
    roi_edges, polygon = region_of_interest(edges)

    # Overlay extracted lane pixels in red on the original image
    overlay = img.copy()
    overlay[roi_edges > 0] = (0, 0, 255)
    cv2.polylines(overlay, polygon, True, (0, 255, 0), 2)

    steps = {
        "1_hsv_mask": mask,
        "2_blurred": blurred,
        "3_canny": edges,
        "4_roi_edges": roi_edges,
        "5_result": overlay,
    }
    for label, im in steps.items():
        cv2.imwrite(os.path.join(out_dir, f"{name}_{label}.jpg"), im)
    print(f"Processed {path} -> {out_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python lane_extractor.py <image> [<image> ...]")
    for p in sys.argv[1:]:
        process(p)
