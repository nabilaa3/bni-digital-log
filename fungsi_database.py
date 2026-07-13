import mysql.connector
import streamlit as st

def get_db_connection():
    """Fungsi untuk membuat koneksi ke Database Cloud Aiven via Streamlit Secrets"""
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        # Tambahkan baris ini jika Anda menggunakan SSL/TLS dari Aiven
        ssl_ca="ca.pem" 
    )

def init_db():
    """Fungsi untuk inisialisasi tabel tamu"""
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
    except mysql.connector.Error as err:
        st.error(f"Error Database: {err}") # Menggunakan st.error agar tampil di aplikasi
