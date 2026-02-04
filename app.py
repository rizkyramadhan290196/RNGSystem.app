import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Mengambil data dari menu "Secrets" secara otomatis
def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Membaca bagian [gcp_service_account] dari Secrets
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Database_RNG_Rizky").get_worksheet(0)

st.title("🎯 RNG DATABASE RIZKY V3")

try:
    sheet = init_connection()
    st.success("✅ BERHASIL TERHUBUNG!")
    
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.text_input("Sesi Jam")
        angka = st.text_input("Angka Keluar")
        
        if st.form_submit_button("SIMPAN DATA"):
            if jam and angka:
                sheet.append_row([str(tgl), jam, angka])
                st.success(f"Angka {angka} tersimpan di Google Sheets!")
            else:
                st.warning("Mohon isi jam dan angka.")
except Exception as e:
    st.error(f"Koneksi Gagal: {e}")
