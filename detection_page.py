import streamlit as st
import tensorflow as tf
from PIL import Image
import os
import requests
import datetime

def show_detection():
    # ---------- TITLE ----------
    st.markdown('<div style="font-size:24px;font-weight:bold;color:green">Deepfake Image Detector</div>', unsafe_allow_html=True)

    # ---------- DOWNLOAD MODEL ----------
    @st.cache_resource
    def download_model(url, path):
        if not os.path.exists(path):
            with requests.get(url, stream=True) as r:
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        return path

    # ---------- PREPROCESS ----------
    def preprocess_image(img, target_size=(224, 224)):
        img = img.convert("RGB").resize(target_size)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, axis=0)
        return img_array / 255.0

    model_url = "https://drive.google.com/uc?export=download&id=1cZgWS_6pL1hIDq03s_bWy7kfMlshhqtS"
    model_path = "model/model_revisi.h5"
    download_model(model_url, model_path)
    model = tf.keras.models.load_model(model_path)

    uploaded_file = st.file_uploader("📂 Upload a face image (jpg/jpeg/png)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        file_size = round(uploaded_file.size / (1024 * 1024), 2)
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**File Name:** {uploaded_file.name}")
        with col2:
            st.markdown(f"**File Size:** {file_size} MB")
        with col3:
            st.markdown(f"**Scanned At:** {current_time}")

        st.markdown("---")
        st.markdown("### Disclaimer")
        st.markdown(
            "<p style='color:gray;font-size:14px;'>"
            "This system provides an estimate of whether an image is real or a deepfake. It is not intended for legal, security, or forensic use."
            "</p>",
            unsafe_allow_html=True,
        )

        image = Image.open(uploaded_file)
        st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)

        input_array = preprocess_image(image)
        pred = model.predict(input_array)[0][0]

        label = "Deepfake" if pred > 0.5 else "Real"
        confidence = float(pred) if pred > 0.5 else 1 - float(pred)
        emoji = "🚨" if pred > 0.5 else "✅"
        color = "#ffe6e6" if pred > 0.5 else "#e6ffea"

        st.markdown(f"""
        <div style='background-color:{color};padding:20px;border-radius:10px;border:1px solid #ccc'>
            <h3>{emoji} Prediction: {label}</h3>
            <p>Confidence Score: <b>{confidence:.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Detection Confidence")
        st.progress(confidence)
