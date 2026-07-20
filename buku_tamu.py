import streamlit as st
from datetime import datetime
import os
from fungsi_database import get_db_connection, init_db
from tampilan import atur_tampilan_bni

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Digital Log Kunjungan BNI", page_icon="🏦", layout="wide")
init_db()
atur_tampilan_bni()

# SIDEBAR (Logo dihapus dari sini)
menu = st.sidebar.selectbox("Menu Navigasi", ["Form Kunjungan", "Buka Rekapitulasi"])

# HALAMAN 1: FORM
if menu == "Form Kunjungan":
    # LOGO DIPINDAH KE TENGAH (Disesuaikan posisinya)
    if os.path.exists("BNI.png"):
        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            st.image("BNI.png", width=200)

    st.markdown("<div class='bni-title'>📝 Buku Tamu</div>", unsafe_allow_html=True)
    with st.form("form_tamu", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nama = col1.text_input("Nama")
        telp = col2.text_input("Nomor Telepon / WA")
        alamat = st.text_area("Alamat")
        tujuan = st.text_input("Tujuan")
        
        if st.form_submit_button("Simpan Data"):
            if nama and telp and alamat:
                from datetime import datetime, timedelta
                waktu_wita = datetime.utcnow() + timedelta(hours=8)
                jam_simpan = waktu_wita.strftime("%H:%M:%S")
                tgl_simpan = waktu_wita.strftime("%Y-%m-%d")

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tabel_tamu (tgl, jam, nama, alamat, telp, tujuan) VALUES (%s, %s, %s, %s, %s, %s)",
                               (tgl_simpan, jam_simpan, nama, alamat, telp, tujuan))
                conn.commit()
                conn.close()
                st.success("Data berhasil disimpan!")
            else: st.error("Mohon lengkapi semua kolom!")

    st.markdown("---")
    st.subheader("👥 Tamu yang Datang Hari Ini")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tgl, jam, nama, alamat, telp, tujuan FROM tabel_tamu WHERE tgl = %s ORDER BY jam DESC", (datetime.now().strftime("%Y-%m-%d"),))
        data = cursor.fetchall()
        conn.close()
        
        if data:
            tabel_output = []
            for r in data:
                jam_formatted = str(r[1])[:8] if r[1] else ""
                tabel_output.append({
                    "Tanggal": r[0], "Jam": jam_formatted, "Nama": r[2], 
                    "Alamat": r[3], "Kontak": r[4], "Tujuan": r[5]
                })
            st.table(tabel_output)
        else:
            st.write("Belum ada data tamu hari ini.")
    except Exception as e:
        st.error(f"Error: {e}")

# HALAMAN 2: REKAPITULASI
else:
    st.markdown("<div class='bni-title'>🔒 Dashboard Rekapitulasi</div>", unsafe_allow_html=True)
    pwd = st.text_input("Masukkan Sandi Admin:", type="password")
    
    if pwd == "admin123":
        st.success("Akses Diterima!") 
        
        c1, c2, c3, c4 = st.columns(4)
        hari = c1.selectbox("Tanggal", ["Semua"] + list(range(1, 32)), index=0)
        bulan = c2.selectbox("Bulan", ["Semua"] + list(range(1, 13)), index=0)
        tahun = c3.selectbox("Tahun", ["Semua", 2025, 2026, 2027], index=0)
        nama_cari = c4.text_input("Cari Nama Tamu:")
        
        if st.button("Cari Sekarang"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                query = "SELECT tgl, jam, nama, alamat, telp, tujuan FROM tabel_tamu WHERE 1=1"
                params = []
                
                if hari != "Semua":
                    query += " AND DAY(tgl) = %s"
                    params.append(hari)
                if bulan != "Semua":
                    query += " AND MONTH(tgl) = %s"
                    params.append(bulan)
                if tahun != "Semua":
                    query += " AND YEAR(tgl) = %s"
                    params.append(tahun)
                
                if nama_cari:
                    query += " AND nama LIKE %s"
                    params.append(f"%{nama_cari}%")
                
                # Menambahkan pengurutan agar data terbaru muncul di atas
                query += " ORDER BY tgl DESC, jam DESC"
                
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                conn.close()
                
                if data:
                    tabel_output = []
                    for r in data:
                        jam_formatted = str(r[1])[:8] if r[1] else ""
                        tabel_output.append({"Tanggal": r[0], "Jam": jam_formatted, "Nama": r[2], "Alamat": r[3], "Kontak": r[4], "Tujuan": r[5]})
                    st.table(tabel_output)
                else:
                    st.info("Tidak ada data ditemukan untuk kriteria tersebut.")
            except Exception as e:
                st.error(f"Error memuat data: {e}")
    elif pwd:
        st.error("Sandi Salah!")
