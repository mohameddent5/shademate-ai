# === ShadeMate AI Real-Time VITA Match Engine ===
import numpy as np
import cv2
import math
import random

# --- VITA LAB Reference Table (Simplified, Can Be Expanded) ---
VITA_SHADES = {
    "A1": (75, 2, 9),
    "A2": (72, 3, 13),
    "A3": (69, 4, 15),
    "B1": (78, 1, 8),
    "B2": (74, 2, 10),
    "C1": (73, 0, 9),
    "C2": (70, 1, 11),
    "D2": (71, 3, 13),
    "D3": (68, 4, 14)
}

# --- ΔE (Delta E) Function for LAB Matching ---
def delta_e(lab1, lab2):
    return math.sqrt((lab1[0] - lab2[0])**2 + (lab1[1] - lab2[1])**2 + (lab1[2] - lab2[2])**2)

# --- Real VITA Matching from Image Path ---
def extract_lab_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or invalid format.")

    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    h, w, _ = lab_image.shape
    cx, cy = w // 2, h // 2
    crop_size = 100
    cropped = lab_image[cy - crop_size // 2:cy + crop_size // 2,
                        cx - crop_size // 2:cx + crop_size // 2]

    L = np.mean(cropped[:, :, 0])
    A = np.mean(cropped[:, :, 1])
    B = np.mean(cropped[:, :, 2])

    return round(L, 1), round(A, 1), round(B, 1)

# --- Match Closest VITA Shade ---
def match_vita_shade(lab):
    closest_shade = None
    min_delta = float("inf")

    for shade, ref_lab in VITA_SHADES.items():
        de = delta_e(lab, ref_lab)
        if de < min_delta:
            min_delta = de
            closest_shade = shade

    return closest_shade, round(min_delta, 2)

# --- Generate Clinical Tips Based on Matched Shade ---
def generate_clinical_tips(tooth_type, restoration_type):
    tips_pool = [
        "Layer ceramics to replicate incisal translucency",
        "Mimic adjacent teeth surface texture for harmony",
        "Use silicone index for consistent layering",
        "Select shade under natural or cross-polarized light",
        "Account for cervical shading in crown margins",
        "Finish restorations with microtexture to scatter light",
        "Choose neutral lighting to avoid chroma distortion",
        "Observe patient under ambient lighting post-op",
        "Polish gently to maintain optical integration"
    ]
    selected_tips = random.sample(tips_pool, 2)
    return selected_tips

# --- Generate Final Report Block ---
def generate_analysis_report(image_path, tooth_type, restoration_type):
    lab = extract_lab_from_image(image_path)
    shade, delta = match_vita_shade(lab)

    if delta <= 2:
        quality = "🟢 Excellent Match"
    elif delta <= 4:
        quality = "🟡 Clinically Acceptable"
    else:
        quality = "🔴 Visibly Mismatched"

    tips = generate_clinical_tips(tooth_type, restoration_type)

    return f"""
## 🦷 ShadeMate AI Report

**📷 Extracted LAB Values**:  L* = {lab[0]} / a* = {lab[1]} / b* = {lab[2]}
**🎯 Closest VITA Shade Match**: `{shade}`  
**🔍 Match Confidence**: {quality} (ΔE = {delta})

---

### ✨ Aesthetic Tips for {restoration_type} on Tooth {tooth_type}:
1. {tips[0]}
2. {tips[1]}

---
*AI-generated shade analysis. No GPT-4. No cloud APIs. 100% edge-run logic.*
"""

# --- Main Application Entry Point ---
def main():
    print("🦷 ShadeMate AI - VITA Shade Matching System")
    print("=" * 50)
    
    # Example demonstration with sample data
    print("\n📋 Demo Mode: Simulating shade analysis...")
    
    # Since we don't have an actual image, let's demonstrate with sample LAB values
    sample_lab = (72, 3, 12)  # Sample LAB values
    shade, delta = match_vita_shade(sample_lab)
    
    print(f"\n📊 Sample LAB Values: L*={sample_lab[0]}, a*={sample_lab[1]}, b*={sample_lab[2]}")
    print(f"🎯 Matched VITA Shade: {shade}")
    print(f"🔍 Delta E: {delta}")
    
    if delta <= 2:
        quality = "🟢 Excellent Match"
    elif delta <= 4:
        quality = "🟡 Clinically Acceptable"
    else:
        quality = "🔴 Visibly Mismatched"
    
    print(f"📈 Match Quality: {quality}")
    
    # Display available VITA shades
    print(f"\n📚 Available VITA Shades in Database:")
    for shade_name, lab_values in VITA_SHADES.items():
        print(f"  {shade_name}: L*={lab_values[0]}, a*={lab_values[1]}, b*={lab_values[2]}")
    
    # Generate sample clinical tips
    tips = generate_clinical_tips("Central Incisor", "Crown")
    print(f"\n✨ Clinical Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")
    
    print(f"\n💡 To analyze an actual image, use:")
    print(f"   result = generate_analysis_report('image_path.jpg', 'tooth_type', 'restoration_type')")

if __name__ == "__main__":
    main()
