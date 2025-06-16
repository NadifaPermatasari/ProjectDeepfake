import streamlit as st

def show_home():
    st.markdown("""
        <div style="text-align: center; padding-top: 20px;">
            <h2 style="font-size: 2rem; font-weight: bold; color: #1a2a4b; margin-bottom: 10px;">
                👋 Welcome to the Deepfake Image Detector
            </h2>
            <p style="font-size: 16.5px; max-width: 700px; margin: 10px auto 20px; line-height: 1.5; color: #333;">
                This application helps you detect whether a facial image has been manipulated using deepfake technology or is authentic
                <br><br>
                Please use the <b>"Detection"</b> menu above to upload an image and view the prediction result.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.image("utils/deepfake.jpg", use_container_width=True)
