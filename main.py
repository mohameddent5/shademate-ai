
import streamlit as st
import base64
import random

st.set_page_config(page_title="ShadeMate AI", page_icon="🦷", layout="wide")

st.title("🦷 ShadeMate AI")
st.markdown("AI-powered dental aesthetic guidance - **Demo Mode** 😎")

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Photo Analysis")
    uploaded_file = st.file_uploader("Upload a smile or tooth photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

with col2:
    st.subheader("🔧 Clinical Parameters")
    tooth = st.selectbox("Select Tooth Number", ["11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43"])
    lighting = st.radio("Lighting Condition", ["Natural Light", "LED", "Intraoral Flash"])
    restoration_type = st.selectbox("Restoration Type", ["Crown", "Veneer", "Composite", "Implant Crown"])

# Convert image to base64 (for future API integration)
def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Enhanced mock AI response
def generate_mock_response(tooth, lighting, restoration_type):
    # More comprehensive shade options
    shades = {
        "A": ["A1", "A2", "A3", "A3.5", "A4"],
        "B": ["B1", "B2", "B3", "B4"],
        "C": ["C1", "C2", "C3", "C4"],
        "D": ["D2", "D3", "D4"]
    }
    
    # Professional dental tips
    tips_database = [
        "Use cross-polarized photography to eliminate surface reflections",
        "Select shade under multiple light sources for accuracy", 
        "Consider adjacent tooth translucency for seamless blending",
        "Map surface texture using high-resolution intraoral photography",
        "Account for gingival color influence on cervical area",
        "Use layered ceramics to replicate natural depth",
        "Finish with micro-texture for optimal light reflection",
        "Consider patient's age-related color changes",
        "Evaluate shade at different times of day",
        "Use silicone index for consistent shade communication"
    ]
    
    # Lighting-specific recommendations
    lighting_notes = {
        "Natural Light": "Ideal for shade matching - most accurate color rendition",
        "LED": "Good consistency but verify with natural light",
        "Intraoral Flash": "May wash out subtle color variations"
    }
    
    # Generate realistic response
    shade_family = random.choice(list(shades.keys()))
    selected_shade = random.choice(shades[shade_family])
    selected_tips = random.sample(tips_database, 2)
    
    # Add tooth position context
    tooth_zone = "anterior" if tooth.startswith(('1', '2')) else "posterior"
    
    return f"""
### 🎯 **Analysis Results**

**📊 VITA Shade Estimate:** `{selected_shade}` 
*Primary shade for tooth {tooth} ({tooth_zone} region)*

**💡 Lighting Assessment:** {lighting_notes[lighting]}

**✨ Clinical Recommendations for {restoration_type}:**
1. **{selected_tips[0]}**
2. **{selected_tips[1]}**

**🔬 Additional Notes:**
- Consider surface texture variations in the {tooth_zone} zone
- Verify shade match under patient's typical lighting conditions
- Document with standardized photography protocol

---
*🤖 This is an AI-generated mock analysis for demonstration purposes*
"""

# Analysis section
st.markdown("---")

if uploaded_file and st.button("🔍 Analyze Photo", type="primary", use_container_width=True):
    with st.spinner("Analyzing dental aesthetics..."):
        # Simulate processing time
        import time
        time.sleep(2)
        
        result = generate_mock_response(tooth, lighting, restoration_type)
        
        st.success("Analysis Complete!")
        st.markdown(result)
        
        # Add download option
        st.download_button(
            label="📄 Download Analysis Report",
            data=result,
            file_name=f"shade_analysis_tooth_{tooth}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("💡 **Pro Tip:** This demo showcases AI capabilities without API costs. Perfect for testing workflows!")
