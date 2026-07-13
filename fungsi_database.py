import mysql.connector
import streamlit as st

def get_db_connection():
    """Koneksi database menggunakan Streamlit Secrets"""
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        ssl_ca="ca.pem"  # Pastikan file ca.pem ada di GitHub Anda
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tabel_tamu (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                tgl DATE, 
                jam TIME, 
                nama VARCHAR(100), 
                alamat TEXT, 
                telp VARCHAR(20), 
                tujuan VARCHAR(150)
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error Database: {e}")
