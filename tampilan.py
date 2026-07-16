import streamlit as st

def atur_tampilan_bni():
    st.markdown("""
        <style>
        /* Sembunyikan tombol Manage app saja */
        [data-testid="stAppDeployButton"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
