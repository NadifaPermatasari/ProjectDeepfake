import streamlit as st

def show_about():
    st.markdown('<div class="title" style="font-size:24px; font-weight:bold; color:#444;">ℹ️ About Us</div>', unsafe_allow_html=True)
    st.write("""
    **Deepfake Image Detector** is a project developed by **Group 5** from the **Department of Business Statistics, Institut Teknologi Sepuluh Nopember (ITS), Indonesia**.  
    This project aims to help the public identify fake or manipulated images (*deepfakes*) that have the potential to mislead, by utilizing **Deep Learning** technology.

    The team consists of **5 members** who collaboratively worked on data collection, model development, evaluation, and web deployment using **Streamlit**.

    We use real and fake image datasets from **Kaggle**, and implement a **Convolutional Neural Network (CNN)** model to detect deepfake images effectively.

    Our team consists of 5 members:
    - Virda Wulandari           (2043221058)
    - Ranti Aninda              (2043221069)
    - Damayanti Zulvita Aisyah  (2043221079)
    - Nadifa Permata sari       (2043221108)  

    We collaboratively worked on data processing, model building, evaluation, and web deployment using **Streamlit**, with datasets obtained from **Kaggle**.
    """)

    st.markdown("---")
    st.markdown("📧 Contact: 2043221108@student.its.ac.id")


