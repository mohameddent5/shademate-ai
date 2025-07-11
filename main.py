import streamlit as st
import cv2
import numpy as np
import base64
import os
from PIL import Image
import tempfile

st.set_page_config(page_title="ShadeMate AI", page_icon="🦷", layout="wide")
st.title("ShadeMate AI 🦷")
st.markdown("**Zero-cost AI Dental Esthetics Assistant** - MVP Edition")

# ===========================
# SECTION 1: MULTI-IMAGE UPLOAD
# ===========================
st.markdown("### 📸 Upload Multiple Smile Images")
uploaded_files = st.file_uploader(
    "Upload frontal, lateral, occlusal, and shade tab photos", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

# ===========================
# SECTION 2: CLINICAL CONTEXT
# ===========================
st.markdown("### 🦷 Clinical Case Context")
tooth_number = st.selectbox("Select Target Tooth", ["11", "12", "13", "21", "22", "23", "31", "41"])
lighting = st.radio("Lighting Used", ["Natural", "LED", "Intraoral Flash"])
restoration_type = st.selectbox("Restoration Type", ["Crown", "Veneer", "Composite", "Implant Crown"])

# ===========================
# SECTION 3: IMAGE PREVIEW
# ===========================
if uploaded_files:
    st.markdown("### 📷 Uploaded Image Previews")
    cols = st.columns(min(3, len(uploaded_files)))
    for i, file in enumerate(uploaded_files):
        cols[i % 3].image(file, caption=file.name, use_column_width=True)

# ===========================
# SECTION 4: SHADE ESTIMATION USING OPENCV (FREE)
# ===========================
def estimate_lab_shade(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    mean_lab = np.mean(img_lab.reshape(-1, 3), axis=0)
    return tuple(map(int, mean_lab))

# ===========================
# SECTION 5: AI MOCK OUTPUT (GPT-4V SIMULATED)
# ===========================
def generate_ai_feedback(tooth, lighting, restoration, lab_values):
    lab_note = f"Estimated LAB: L*={lab_values[0]}, a*={lab_values[1]}, b*={lab_values[2]}"
    suggestions = [
        "Use cross-polarized filters to minimize reflections",
        "Select shade under multiple light sources",
        "Verify shade with neighboring teeth in mind",
        "Consider ceramic layering for natural depth",
        "Use silicone index to record texture and contour",
        "Document with retracted, color-calibrated images"
    ]
    chosen = np.random.choice(suggestions, size=2, replace=False)
    region = "anterior" if tooth.startswith("1") or tooth.startswith("2") else "posterior"

    return f"""
### 🔮 ShadeMate AI Analysis Result

**Tooth:** {tooth} ({region} region)  
**Lighting:** {lighting}  
**Restoration Type:** {restoration}  
**{lab_note}**  

### ✨ Aesthetic Suggestions:
1. {chosen[0]}
2. {chosen[1]}

*Note: AI result is approximate. For clinical use, validate under calibrated light.*
"""

# ===========================
# SECTION 6: RUN ANALYSIS
# ===========================
if uploaded_files and st.button("🔍 Analyze Images"):
    with st.spinner("Running free AI-based shade analysis..."):
        primary_img = uploaded_files[0]  # Use first image for simplicity
        lab = estimate_lab_shade(primary_img)
        result = generate_ai_feedback(tooth_number, lighting, restoration_type, lab)

        st.success("Analysis Complete!")
        st.markdown(result)

        st.download_button(
            label="📄 Download Report",
            data=result,
            file_name=f"ShadeMate_Report_{tooth_number}.txt",
            mime="text/plain"
        )

# ===========================
# SECTION 7: FOOTER
# ===========================
st.markdown("---")
st.markdown("Made with ❤️ by Mohamed | Powered by OpenCV + Streamlit + Science")

