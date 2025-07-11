
import streamlit as st
import numpy as np
import cv2
import math
import random
from PIL import Image
import io

# --- VITA LAB Reference Table ---
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

# --- Extract LAB from uploaded image ---
def extract_lab_from_uploaded_image(image_bytes):
    # Convert PIL image to OpenCV format
    image = Image.open(io.BytesIO(image_bytes))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    lab_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2LAB)
    h, w, _ = lab_image.shape
    cx, cy = w // 2, h // 2
    crop_size = min(100, h//2, w//2)  # Adjust crop size for smaller images
    
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

# --- Generate Clinical Tips ---
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
    return random.sample(tips_pool, 2)

# --- Streamlit App ---
def main():
    st.set_page_config(
        page_title="ShadeMate AI",
        page_icon="🦷",
        layout="wide"
    )
    
    st.title("🦷 ShadeMate AI - VITA Shade Matching System")
    st.markdown("*AI-powered dental shade analysis using CIELAB color space*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📷 Image Analysis")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload a dental image", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a high-quality image of the tooth for shade analysis"
        )
        
        # Input fields
        tooth_type = st.selectbox(
            "Tooth Type",
            ["Central Incisor", "Lateral Incisor", "Canine", "Premolar", "Molar"]
        )
        
        restoration_type = st.selectbox(
            "Restoration Type",
            ["Crown", "Veneer", "Filling", "Bridge", "Implant"]
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Shade", type="primary"):
                with st.spinner("Analyzing shade..."):
                    try:
                        # Extract LAB values
                        lab = extract_lab_from_uploaded_image(uploaded_file.getvalue())
                        shade, delta = match_vita_shade(lab)
                        
                        # Store results in session state
                        st.session_state.analysis_results = {
                            'lab': lab,
                            'shade': shade,
                            'delta': delta,
                            'tooth_type': tooth_type,
                            'restoration_type': restoration_type
                        }
                        
                    except Exception as e:
                        st.error(f"Error analyzing image: {str(e)}")
    
    with col2:
        st.header("📊 Analysis Results")
        
        # Display results if available
        if hasattr(st.session_state, 'analysis_results'):
            results = st.session_state.analysis_results
            
            # LAB Values
            st.subheader("🎨 Color Analysis")
            col_l, col_a, col_b = st.columns(3)
            with col_l:
                st.metric("L* (Lightness)", f"{results['lab'][0]}")
            with col_a:
                st.metric("a* (Green-Red)", f"{results['lab'][1]}")
            with col_b:
                st.metric("b* (Blue-Yellow)", f"{results['lab'][2]}")
            
            # Shade Match
            st.subheader("🎯 VITA Shade Match")
            st.markdown(f"### **{results['shade']}**")
            
            # Match Quality
            if results['delta'] <= 2:
                quality = "🟢 Excellent Match"
                quality_color = "green"
            elif results['delta'] <= 4:
                quality = "🟡 Clinically Acceptable"
                quality_color = "orange"
            else:
                quality = "🔴 Visibly Mismatched"
                quality_color = "red"
            
            st.markdown(f"**Match Quality:** {quality}")
            st.metric("Delta E (ΔE)", f"{results['delta']}")
            
            # Clinical Tips
            st.subheader("✨ Clinical Recommendations")
            tips = generate_clinical_tips(results['tooth_type'], results['restoration_type'])
            for i, tip in enumerate(tips, 1):
                st.markdown(f"{i}. {tip}")
        
        else:
            st.info("Upload an image and click 'Analyze Shade' to see results here.")
    
    # VITA Shade Reference
    st.header("📚 VITA Shade Reference")
    
    # Create columns for shade display
    cols = st.columns(len(VITA_SHADES))
    for i, (shade_name, lab_values) in enumerate(VITA_SHADES.items()):
        with cols[i]:
            st.markdown(f"**{shade_name}**")
            st.text(f"L*: {lab_values[0]}")
            st.text(f"a*: {lab_values[1]}")
            st.text(f"b*: {lab_values[2]}")
    
    # Demo Mode
    st.header("🧪 Demo Mode")
    if st.button("Run Demo Analysis"):
        sample_lab = (72, 3, 12)
        shade, delta = match_vita_shade(sample_lab)
        
        st.success(f"Demo Results: LAB({sample_lab[0]}, {sample_lab[1]}, {sample_lab[2]}) → VITA {shade} (ΔE: {delta})")

if __name__ == "__main__":
    main()
