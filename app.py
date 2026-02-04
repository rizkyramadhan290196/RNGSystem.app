import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random

# --- KONFIGURASI KONEKSI DATABASE ---
def init_connection():
    # Mengambil izin akses ke Google Sheets dan Google Drive
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Mengambil data dari Secrets (Format TOML yang kita buat tadi)
    creds_dict = st.secrets["gcp_service_account"]
    
    # Membuat kredensial dari info yang ada di Secrets
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # MEMBUKA SHEET DENGAN NAMA SPESIFIK MILIK RIZKY
    return client.open("Database_RNG_Rizky").get_worksheet(0)

# Inisialisasi koneksi ke sheet
try:
    sheet = init_connection()
except Exception as e:
    st.error(f"Koneksi Gagal! Pastikan nama sheet benar dan email service account sudah di-'Share' sebagai Editor. Error: {e}")
    st.stop()

st.set_page_config(page_title="RNG V3 PRO - RIZKY", layout="centered")

st.title("🎯 RNG SYSTEM STATISTIK V3")
st.write("Database: `Database_RNG_Rizky`")

tab1, tab2, tab3 = st.tabs(["📊 INPUT DATA", "🔥 ANALISA HOT/COLD", "🔮 PREDIKSI"])

# --- TAB 1: INPUT DATA ---
with tab1:
    st.subheader("Input Hasil Result")
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.text_input("Sesi Jam (Manual)", placeholder="Contoh: 21.00 atau Sesi 1")
        angka = st.text_input("Angka Keluar (Contoh: 1234)")
        
        submit = st.form_submit_button("SIMPAN KE GOOGLE SHEETS")
        
        if submit:
            if jam and angka:
                try:
                    # Menambahkan baris baru ke Google Sheets
                    sheet.append_row([str(tgl), jam, str(angka)])
                    st.success(f"✅ Data Berhasil Disimpan ke Google Sheets!")
                except Exception as e:
                    st.error(f"Gagal menyimpan: {e}")
            else:
                st.warning("⚠️ Mohon isi Jam dan Angka terlebih dahulu!")

# --- TAB 2: ANALISA HOT & COLD ---
with tab2:
    st.subheader("Analisa Angka (Berdasarkan Data Real)")
    try:
        data = sheet.get_all_records()
        if data:
            df = pd.DataFrame(data)
            # Analisa digit terakhir (Ekor)
            df['Digit_Terakhir'] = df['Angka'].astype(str).str[-1]
            
            counts = df['Digit_Terakhir'].value_counts()
            hot_nums = counts.head(3)
            cold_nums = counts.tail(3)
            
            col1, col2 = st.columns(2)
            with col1:
                st.error("🔥 ANGKA HOT (Ekor)")
                for val, count in hot_nums.items():
                    st.write(f"Digit {val}: Muncul {count}x")
            
            with col2:
                st.info("❄️ ANGKA COLD (Ekor)")
                for val, count in cold_nums.items():
                    st.write(f"Digit {val}: Muncul {count}x")
        else:
            st.info("Belum ada data di Google Sheets untuk dianalisa.")
    except:
        st.write("Gagal memuat data analisa. Pastikan kolom 'Angka' sudah ada isinya.")

# --- TAB 3: PREDIKSI ---
with tab3:
    st.subheader("Generator Prediksi Pintar")
    tipe = st.selectbox("Pilih Tipe Prediksi", ["2D", "3D", "4D", "5D"])
    
    if st.button("🔥 GENERATE PREDIKSI"):
        st.write(f"### Rekomendasi {tipe}:")
        for i in range(1, 11):
            # Simulasi RNG sederhana yang bisa dikembangkan lebih lanjut
            res = "".join([str(random.randint(0,9)) for _ in range(int(tipe[0]))])
            st.code(f"Line {i}: {res}")

st.divider()
st.caption("Sistem RNG Terhubung Otomatis ke Google Sheets Rizky.")
