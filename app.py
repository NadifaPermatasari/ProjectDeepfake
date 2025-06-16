import streamlit as st
from home import show_home
from pages.detection_page import show_detection
from pages.about_page import show_about
from utils.style import set_custom_style

st.set_page_config(page_title="Deepfake Image Detector", layout="wide")
set_custom_style()

if "page" not in st.session_state:
    st.session_state.page = "home"

def navigate_to(page_name):
    st.session_state.page = page_name

# --- Custom CSS ---
st.markdown("""
    <style>
    .nav-buttons {
        display: flex;
        justify-content: center; /* Tetap di tengah */
        padding: 12px 0px; /* Padding vertikal tetap, padding horizontal dihilangkan */
        background-color: transparent; /* Ubah menjadi transparan */
        position: sticky;
        top: 0;
        border-bottom: none; /* Hilangkan border bawah */
        z-index: 999;
        width: 100%; /* Pastikan div mengambil lebar penuh */
        box-shadow: none; /* Hilangkan bayangan */
    }
    .stButton>button {
        margin: 0 10px; /* Margin kiri dan kanan 10px untuk spasi antar tombol */
        border-radius: 6px;
        background-color: white; /* Biarkan tombol tetap berwarna putih */
        border: 1px solid #1a2a4b;
        color: #1a2a4b;
        font-weight: 500;
        transition: 0.3s ease;
        min-width: 120px; /* Opsional: berikan lebar minimum agar tombol lebih seragam */
        padding: 8px 15px; /* Opsional: sesuaikan padding tombol */
    }
    .stButton>button:hover {
        background-color: #4e3ff2;
        color: white;
    }
    /* Streamlit's default container padding can affect centering.
       We'll remove horizontal padding from the top 'block-container' if layout is 'wide'
       to allow .nav-buttons to span full width and center effectively.
       This targets a specific Streamlit internal class, might need adjustment with future versions.
    */
    .st-emotion-cache-h4yq0v { /* Ini adalah contoh class ID Streamlit untuk main block. Cari ID yang benar di inspeksi elemen browser Anda. */
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .st-emotion-cache-z5fcl4 { /* Ini juga bisa jadi main block container */
        padding-left: 0rem;
        padding-right: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Render Navigasi ---
# Gunakan st.container untuk membungkus nav-buttons agar lebih mudah dikontrol layoutnya
with st.container():
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    
    col_home, col_detection, col_about = st.columns(3)

    with col_home:
        st.button("🏠 Home", on_click=navigate_to, args=("home",), key="nav_home")
    with col_detection:
        st.button("🧠 Detection", on_click=navigate_to, args=("detection",), key="nav_detection")
    with col_about:
        st.button("ℹ️ About Us", on_click=navigate_to, args=("about",), key="nav_about")
    
    st.markdown('</div>', unsafe_allow_html=True)


# --- Routing
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "detection":
    show_detection()
elif st.session_state.page == "about":
    show_about()