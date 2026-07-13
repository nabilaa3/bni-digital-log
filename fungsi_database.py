import mysql.connector
import os
from dotenv import load_dotenv

# Muat variabel rahasia dari file .env
load_dotenv()

def get_db_connection():
    """Fungsi untuk membuat koneksi ke Database Cloud Aiven"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def init_db():
    """Fungsi untuk inisialisasi tabel tamu jika belum ada di database"""
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
        print(f"Error Database: {err}")