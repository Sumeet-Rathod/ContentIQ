import cv2
import numpy as np
from typing import Dict, Any, List

def score_thumbnail(image_bytes: bytes) -> Dict[str, Any]:
    """
    Score social media thumbnail quality using OpenCV Computer Vision:
    1. Brightness: Mean luminance normalized, penalizing under/over exposure.
    2. Contrast: Standard deviation of pixel intensities across gray channels.
    3. Sharpness: Laplacian variance metric (edge focus & blur detection).
    4. Colourfulness: Hasler and Süsstrunk (2003) perceptual color metric.
    5. Composition: Edge distribution aligned with Rule of Thirds power points.
    """
    # Decode image from memory
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image file. Please upload a valid JPG, PNG, or WebP.")
        
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Brightness Metric
    # Optimal luminance is between 0.45 and 0.75
    mean_lum = float(np.mean(gray)) / 255.0
    if 0.40 <= mean_lum <= 0.75:
        brightness_score = 1.0 - (abs(mean_lum - 0.58) / 0.58) * 0.5
    elif mean_lum < 0.40:
        brightness_score = max(0.1, mean_lum / 0.40)
    else:
        brightness_score = max(0.1, (1.0 - mean_lum) / 0.25)
    brightness_score = float(np.clip(brightness_score, 0.05, 1.0))
    
    # 2. Contrast Metric
    # High standard deviation represents dynamic range
    std_lum = float(np.std(gray))
    contrast_score = float(np.clip(std_lum / 65.0, 0.05, 1.0))
    
    # 3. Sharpness Metric (Laplacian Variance)
    # Detects blurriness vs crisp high-frequency edges
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    lap_var = float(laplacian.var())
    sharpness_score = float(np.clip(lap_var / 500.0, 0.05, 1.0))
    
    # 4. Colourfulness Metric (Hasler & Süsstrunk)
    # rg = R - G, yb = 0.5*(R + G) - B
    (B, G, R) = cv2.split(img.astype("float"))
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)
    std_rg, mean_rg = np.std(rg), np.mean(rg)
    std_yb, mean_yb = np.std(yb), np.mean(yb)
    std_root = np.sqrt((std_rg ** 2) + (std_yb ** 2))
    mean_root = np.sqrt((mean_rg ** 2) + (mean_yb ** 2))
    colorfulness_raw = std_root + (0.3 * mean_root)
    # 40-70 is moderately colorful; >80 is vibrant
    colourfulness_score = float(np.clip(colorfulness_raw / 60.0, 0.05, 1.0))
    
    # 5. Composition Metric (Rule of Thirds Edge Energy)
    # Measure edge concentration near the 1/3 and 2/3 horizontal and vertical intersection lines
    edges = cv2.Canny(gray, 50, 150)
    total_edges = float(np.sum(edges > 0)) + 1e-5
    
    # Define rule of thirds regions (middle third bands)
    h_third_1, h_third_2 = int(height / 3), int(2 * height / 3)
    w_third_1, w_third_2 = int(width / 3), int(2 * width / 3)
    margin_h = max(2, int(height * 0.08))
    margin_w = max(2, int(width * 0.08))
    
    mask = np.zeros_like(edges)
    # Horizontal power lines
    mask[max(0, h_third_1 - margin_h):min(height, h_third_1 + margin_h), :] = 1
    mask[max(0, h_third_2 - margin_h):min(height, h_third_2 + margin_h), :] = 1
    # Vertical power lines
    mask[:, max(0, w_third_1 - margin_w):min(width, w_third_1 + margin_w)] = 1
    mask[:, max(0, w_third_2 - margin_w):min(width, w_third_2 + margin_w)] = 1
    
    power_edges = float(np.sum(edges[mask > 0] > 0))
    composition_ratio = power_edges / total_edges
    composition_score = float(np.clip(composition_ratio * 2.2, 0.1, 1.0))
    
    # Overall Score (Weighted combination)
    overall_normalized = (
        0.20 * brightness_score +
        0.20 * contrast_score +
        0.25 * sharpness_score +
        0.20 * colourfulness_score +
        0.15 * composition_score
    )
    overall_percentage = round(overall_normalized * 100, 1)
    
    # Actionable suggestions based on actual measurements
    recommendations = []
    if brightness_score < 0.55:
        if mean_lum < 0.40:
            recommendations.append("Thumbnail is underexposed. Boost exposure/shadows so subjects are clear on mobile screens.")
        else:
            recommendations.append("Thumbnail highlights are washed out. Lower exposure or increase shadow depth.")
    if contrast_score < 0.60:
        recommendations.append("Low tonal contrast. Increase dynamic range between text/subject and background.")
    if sharpness_score < 0.55:
        recommendations.append("Image lacks high-frequency focus. Ensure subject is tack-sharp and avoid compression blur.")
    if colourfulness_score < 0.50:
        recommendations.append("Color saturation is subdued. Vibrancy and saturated accents attract significantly higher CTR.")
    if composition_score < 0.55:
        recommendations.append("Key visual elements are off-grid. Align focal subjects with the Rule-of-Thirds power lines.")
        
    if not recommendations:
        recommendations.append("Outstanding visual quality! Balanced contrast, sharp focus, vibrant palette, and well-framed composition.")
        
    return {
        "dimensions": f"{width}x{height}",
        "brightness": round(brightness_score, 2),
        "contrast": round(contrast_score, 2),
        "sharpness": round(sharpness_score, 2),
        "colourfulness": round(colourfulness_score, 2),
        "composition": round(composition_score, 2),
        "overall_score": overall_percentage,
        "recommendations": recommendations,
        "metrics": [
            {"name": "Brightness", "score": round(brightness_score, 2), "percentage": int(brightness_score * 100)},
            {"name": "Contrast", "score": round(contrast_score, 2), "percentage": int(contrast_score * 100)},
            {"name": "Sharpness", "score": round(sharpness_score, 2), "percentage": int(sharpness_score * 100)},
            {"name": "Colourfulness", "score": round(colourfulness_score, 2), "percentage": int(colourfulness_score * 100)},
            {"name": "Composition", "score": round(composition_score, 2), "percentage": int(composition_score * 100)}
        ]
    }
