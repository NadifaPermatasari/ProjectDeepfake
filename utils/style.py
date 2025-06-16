import streamlit as st
import base64

def set_custom_style():
    with open("utils/bg.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .block-container {{
            max-width: 800px;
            margin: auto;
            padding: 3rem 2rem;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }}
        .title {{
            text-align: center;
            font-size: 2.8rem;
            color: #1a2a4b;
            font-weight: bold;
        }}
        .subtitle {{
            text-align: center;
            font-size: 1.2rem;
            color: #555;
            margin-bottom: 2rem;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
