import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# Fungsi untuk koneksi otomatis baca file
def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Membaca file kunci.json yang sudah kamu buat di GitHub
    with open('kunci.json') as f:
        info_kunci = json.load(f)
    
    creds = Credentials.from_service_account_info(info_kunci, scopes=scope)
    client = gspread.authorize(creds)
    # Pastikan nama Google Sheets kamu tepat: Database_RNG_Rizky
    return client.open("Database_RNG_Rizky").get_worksheet(0)

st.set_page_config(page_title="DATABASE RIZKY V3", layout="centered")
st.title("🎯 DATABASE RIZKY V3")

try:
    sheet = init_connection()
    st.success("✅ KONEKSI BERHASIL!")
    
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.text_input("Sesi Jam")
        angka = st.text_input("Angka Keluar")
        
        if st.form_submit_button("SIMPAN DATA"):
            if jam and angka:
                sheet.append_row([str(tgl), jam, angka])
                st.balloons()
                st.success(f"Mantap! Angka {angka} tersimpan.")
            else:
                st.warning("Isi semua kolom ya.")
except Exception as e:
    st.error(f"Gagal memuat: {e}")
