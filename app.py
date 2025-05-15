import streamlit as st
import requests
from io import BytesIO

# --- Page Config ---
st.set_page_config(page_title="VR-Heart Inference", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        .title {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .subtext {
            text-align: center;
            color: gray;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 1.1em;
            padding: 0.6em 1.2em;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🫀 VR-Heart Inference Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Upload DICOMs ZIP → GPU Inference → Get Results Instantly</div>', unsafe_allow_html=True)

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload your DICOM ZIP file", type=["zip"])

# --- Inference Button ---
if uploaded_file and st.button("🚀 Run Inference"):
    with st.spinner("⏳ Running inference on GPU... this may take a minute..."):
        try:
            response = requests.post(
                "https://giladgressel--vr-heart-backend-fastapi-app.modal.run/process/",
                files={"file": uploaded_file},
                timeout=900  # 15 minutes max
            )

            if response.status_code == 200:
                st.success("✅ Inference complete! Download your results below:")
                st.download_button(
                    label="📦 Download Results ZIP",
                    data=BytesIO(response.content),
                    file_name="vrheart_results.zip",
                    mime="application/zip"
                )
            else:
                st.error(f"❌ Inference failed! Server responded with: {response.status_code}")
                st.text_area("Error Details", response.text, height=150)
        except Exception as e:
            st.error("⚠️ An unexpected error occurred.")
            st.text_area("Exception", str(e), height=150)

# Optional footer
st.markdown("""<hr><p style='text-align: center; color: gray;'>© 2025 VR-Heart | Powered by Modal & Hugging Face</p>""", unsafe_allow_html=True)
