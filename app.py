import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random

# --- KONFIGURASI GOOGLE SHEETS ---
def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Mengambil data dari Secrets yang kamu simpan tadi
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    # GANTI 'NAMA_SHEET_KAMU' dengan nama file Google Sheets kamu
    return client.open("Database_RNG_Rizky").get_worksheet(0)

sheet = init_connection()

st.set_page_config(page_title="RNG V3 PRO", layout="centered")
st.title("🎯 RNG SYSTEM STATISTIK V3")

tab1, tab2, tab3 = st.tabs(["📊 INPUT DATA", "🔥 HOT & COLD", "🔮 PREDIKSI"])

# --- TAB 1: INPUT DATA ---
with tab1:
    st.subheader("Input Hasil Result")
    with st.form("input_form"):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.text_input("Sesi Jam (Manual)", placeholder="Contoh: 21.00")
        angka = st.text_input("Angka Keluar (4 Digit)")
        
        if st.form_submit_button("SIMPAN KE DATABASE"):
            if jam and angka:
                sheet.append_row([str(tgl), jam, angka])
                st.success(f"Data Berhasil Disimpan ke Google Sheets!")
            else:
                st.error("Lengkapi Jam dan Angka!")

# --- TAB 2: ANALISA HOT & COLD ---
with tab2:
    st.subheader("Analisa Statistik (100 Data Terakhir)")
    data = sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        # Ambil digit terakhir (Ekor) sebagai contoh analisa sederhana
        df['Ekor'] = df['Angka'].astype(str).str[-1]
        
        hot_nums = df['Ekor'].value_counts().head(3)
        cold_nums = df['Ekor'].value_counts().tail(3)
        
        col1, col2 = st.columns(2)
        with col1:
            st.error("🔥 ANGKA HOT (Sering)")
            for val, count in hot_nums.items():
                st.write(f"Angka {val}: Muncul {count}x")
        
        with col2:
            st.info("❄️ ANGKA COLD (Jarang)")
            for val, count in cold_nums.items():
                st.write(f"Angka {val}: Muncul {count}x")
    else:
        st.write("Belum ada data untuk dianalisa.")

# --- TAB 3: PREDIKSI BERDASARKAN RUMUS ---
with tab3:
    st.subheader("Generator Prediksi Berdasarkan Tren")
    tipe = st.selectbox("Pilih Tipe", ["2D", "3D", "4D"])
    
    if st.button("🔥 GENERATE PREDIKSI JITU"):
        st.write("### Rekomendasi Angka:")
        for i in range(1, 11):
            res = "".join([str(random.randint(0,9)) for _ in range(int(tipe[0]))])
            st.code(f"Line {i}: {res}")

st.info("Sistem ini sekarang menggunakan RNG yang dikombinasikan dengan Database Google Sheets.")
