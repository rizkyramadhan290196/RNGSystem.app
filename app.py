import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# Nama file sesuai dengan yang kamu upload di screenshot terakhir
NAMA_FILE_JSON = "rng-database-486403-1313e482fc6d.json"

def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Membaca file kunci asli tanpa edit manual
    with open(NAMA_FILE_JSON) as f:
        info_kunci = json.load(f)
    creds = Credentials.from_service_account_info(info_kunci, scopes=scope)
    return gspread.authorize(creds).open("Database_RNG_Rizky").get_worksheet(0)

st.title("🎯 DATABASE RIZKY V3")

try:
    sheet = init_connection()
    st.success("✅ MANTAP! KONEKSI BERHASIL.")
    
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.text_input("Sesi Jam")
        angka = st.text_input("Angka Keluar")
        
        if st.form_submit_button("SIMPAN DATA"):
            if jam and angka:
                sheet.append_row([str(tgl), jam, angka])
                st.balloons()
                st.success(f"Berhasil! Angka {angka} sudah masuk ke Sheets.")
            else:
                st.warning("Tolong isi jam dan angka dulu ya.")
except Exception as e:
    st.error(f"Waduh, masih ada kendala: {e}")
