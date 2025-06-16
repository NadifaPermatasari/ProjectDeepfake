import streamlit as st
import requests
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

from home import show_home
from pages.detection_page import show_detection
from pages.about_page import show_about

# ---------- KONFIGURASI HALAMAN & STYLING ----------
st.set_page_config(
    page_title="Deepfake Image Detector - Kelompok 5 Statistika Bisnis ITS",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed" # Pastikan ini diatur ke "collapsed"
)

# Custom CSS Anda yang sudah ada untuk tampilan latar belakang, tata letak, dan navigasi kustom
st.markdown("""
    <style>
    /* Latar Belakang Utama Aplikasi */
    .stApp {
        background-color: #f0f2f5;
        background-image: url("https://www.transparenttextures.com/patterns/clean-textile.png");
        background-attachment: fixed;
        background-size: cover;
    }

    /* Kontainer Utama Konten */
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        margin-left: auto;
        margin-right: auto;
    }

    /* Header Aplikasi */
    .title {
        font-size: 3.2em;
        text-align: center;
        color: #1a2a4b;
        margin-top: 15px;
        margin-bottom: 10px;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        font-size: 1.15em;
        color: #555555;
        margin-bottom: 40px;
        line-height: 1.6;
    }

    /* Styling Umum untuk Elemen Streamlit (misalnya, teks default, label) */
    .stText, .stMarkdown, .stSubheader {
        color: #333333;
    }

    /* File Uploader Styling */
    .stFileUploader label {
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .stFileUploader div[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #a0a0a0;
        border-radius: 10px;
        padding: 25px;
        background-color: #fcfcfc;
        color: #666666;
        transition: all 0.3s ease;
    }
    .stFileUploader div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #007bff;
        background-color: #e6f7ff;
    }
    .stFileUploader div[data-testid="stFileUploaderDropzone"] svg {
        color: #888888;
    }

    /* Tombol Umum */
    .stButton>button {
        background-color: #007bff;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 1.1em;
        width: fit-content;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Hasil Prediksi */
    .prediction-box {
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
        border: 2px solid;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    .prediction-header {
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .confidence-text {
        font-size: 1.4em;
        font-weight: bold;
        margin-top: 15px;
        color: #333;
    }

    /* Expander */
    .stExpander div[data-testid="stExpanderTitle"] {
        font-weight: bold;
        color: #007bff;
        font-size: 1.1em;
    }
    .stExpander div[data-testid="stExpanderContent"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #e9ecef;
    }

    /* Progress Bar */
    .stProgress .st-cr {
        background-color: #e0e0e0;
        height: 10px;
        border-radius: 5px;
    }
    .stProgress .st-cf {
        background-color: #28a745;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 60px;
        font-size: 0.9em;
        color: #7f8c8d;
        padding-top: 20px;
        border-top: 1px solid #eeeeee;
    }

    /* Animasi */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* --- NAVIGASI KHUSUS (RATA TENGAH HORIZONTAL) --- */
    .nav-buttons-container {
        display: flex;
        justify-content: center; /* Ini yang membuat tombol rata tengah horizontal */
        padding: 12px 30px;
        background-color: transparent; /* Menghilangkan kotak putih */
        position: sticky;
        top: 0;
        border-bottom: none; /* Menghilangkan garis bawah */
        z-index: 999;
        width: 100%;
        box-shadow: none; /* Menghilangkan bayangan */
    }
    /* Styling tombol di dalam navigasi */
    .nav-buttons-container .stButton>button {
        margin: 0 15px; /* Spasi antar tombol secara horizontal */
        border: 1px solid #007bff; /* Border biru ITS */
        color: #007bff; /* Teks biru ITS */
        background-color: white; /* Latar belakang putih */
    }
    .nav-buttons-container .stButton>button:hover {
        background-color: #007bff; /* Latar belakang biru saat hover */
        color: white; /* Teks putih saat hover */
    }

    /* Menghilangkan padding default dari Streamlit di layout wide
       agar .nav-buttons-container dapat membentang penuh dan rata tengah secara presisi.
       PERHATIAN: Class ID ini (st-emotion-cache-xxxxxx) sering berubah antar versi Streamlit.
       Jika navigasi tidak sejajar dengan benar, gunakan "Inspect Element" di browser
       untuk menemukan class ID yang benar dari div utama yang membungkus konten.
    */
    .st-emotion-cache-h4yq0v, .st-emotion-cache-z5fcl4 {
        padding-left: 0rem;
        padding-right: 0rem;
    }

    </style>
""", unsafe_allow_html=True)

# Inisialisasi session_state untuk navigasi
if "page" not in st.session_state:
    st.session_state.page = "home"

def navigate_to(page_name):
    st.session_state.page = page_name

# --- Render Navigasi Horizontal ---
with st.container():
    st.markdown('<div class="nav-buttons-container">', unsafe_allow_html=True)
    
    # Tombol navigasi
    st.button("🏠 Home", on_click=navigate_to, args=("home",), key="nav_home")
    st.button("🧠 Detection", on_click=navigate_to, args=("detection",), key="nav_detection")
    st.button("ℹ️ About Us", on_click=navigate_to, args=("about",), key="nav_about")
    
    st.markdown('</div>', unsafe_allow_html=True)


# --- Routing untuk menampilkan halaman sesuai pilihan ---
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "detection":
    show_detection()
elif st.session_state.page == "about":
    show_about()