import streamlit as st

def atur_tampilan_bni():
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa; }
        .bni-title { color: #005E6A; font-weight: 800; font-size: 32px; border-bottom: 3px solid #E55300; padding-bottom: 10px; margin-bottom: 20px; }
        div[data-testid="stForm"] { background-color: #ffffff; padding: 30px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        div.stButton > button { background-color: #E55300 !important; color: white !important; width: 100%; border-radius: 8px; font-weight: bold; }
        div.stButton > button:hover { background-color: #b34100 !important; }
        </style>
    """, unsafe_allow_html=True)