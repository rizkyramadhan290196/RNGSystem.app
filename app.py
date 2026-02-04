import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. KONEKSI DATABASE ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    with open(NAMA_KUNCI) as f:
        info_kunci = json.load(f)
    creds = Credentials.from_service_account_info(info_kunci, scopes=scope)
    return gspread.authorize(creds).open("Database_RNG_Rizky").get_worksheet(0)

# --- 2. FUNGSI LOGIKA (BBFS & RNG) ---
def get_bbfs(digits, limit):
    if not digits: return []
    # Membuat semua kombinasi yang mungkin
    all_combos = [''.join(p) for p in itertools.permutations(digits, len(digits))]
    random.shuffle(all_combos) # Simulasi RNG untuk urutan terbaik
    return all_combos[:limit]

# --- 3. UI DASHBOARD ---
st.set_page_config(page_title="RIZKY RNG PRO V3", layout="wide")
st.title("🎯 RIZKY SMART RNG SYSTEM V3")

try:
    sheet = init_connection()
    all_data = sheet.get_all_values()
    df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame()

    tab1, tab2, tab3, tab4 = st.tabs(["📥 INPUT", "📊 STATISTIK", "🔮 PREDIKSI", "🎲 BBFS PRO"])

    # --- TAB 1: INPUT DATA ---
    with tab1:
        with st.form("input_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            tgl = col1.date_input("Tanggal", datetime.now())
            jam = col2.text_input("Sesi Jam (Contoh: 14.00)")
            angka = st.text_input("Angka Keluar (4 Digit)")
            if st.form_submit_button("SIMPAN DATA"):
                if jam and angka:
                    sheet.append_row([str(tgl), jam, angka])
                    st.balloons()
                    st.success(f"Data {angka} tersimpan!")
                else: st.warning("Lengkapi data!")

    # --- TAB 2: STATISTIK & GRAFIK ---
    with tab2:
        if not df.empty:
            st.subheader("Analisis Statistik Angka")
            # Ambil digit terakhir dari setiap angka keluar
            df['LastDigit'] = df.iloc[:, 2].str[-1]
            count_data = df['LastDigit'].value_counts().reset_index()
            count_data.columns = ['Angka', 'Frekuensi']
            
            fig = px.bar(count_data, x='Angka', y='Frekuensi', color='Frekuensi', title="Frekuensi Kemunculan Digit Terakhir")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("Belum ada data untuk dianalisis.")

    # --- TAB 3: PREDIKSI (2D - 5D) ---
    with tab3:
        st.subheader("🔮 Ramuan Prediksi RNG")
        tipe_prediksi = st.selectbox("Pilih Tipe Prediksi", ["2D", "3D", "4D", "5D"])
        
        if not df.empty:
            last_num = df.iloc[-1, 2]
            st.write(f"Acuan Data Terakhir: **{last_num}**")
            
            # Algoritma Prediksi Sederhana berbasis Hot Number
            hot_digit = df.iloc[:, 2].str[-1].mode()[0] if not df.empty else "5"
            
            if tipe_prediksi == "2D": hasil = f"{random.randint(0,9)}{hot_digit}"
            elif tipe_prediksi == "3D": hasil = f"{random.randint(0,9)}{random.randint(0,9)}{hot_digit}"
            elif tipe_prediksi == "4D": hasil = f"{random.randint(10,99)}{random.randint(0,9)}{hot_digit}"
            else: hasil = f"{random.randint(10,99)}{random.randint(10,99)}{hot_digit}"
            
            st.metric(f"Prediksi {tipe_prediksi} Terbaik", hasil)
        else: st.warning("Input data dulu di Tab 1!")

    # --- TAB 4: BBFS PRO (10-120) ---
    with tab4:
        st.subheader("🎲 BBFS Smart Generator")
        input_bbfs = st.text_input("Masukkan Angka Main (Contoh: 1234)")
        jumlah_urutan = st.select_slider("Jumlah Urutan Terbaik", options=[10, 30, 60, 90, 120])
        
        if st.button("Generate BBFS"):
            if input_bbfs:
                hasil_bbfs = get_bbfs(input_bbfs, jumlah_urutan)
                st.write(f"Menampilkan **{len(hasil_bbfs)}** kombinasi terbaik:")
                st.info(", ".join(hasil_bbfs))
            else: st.warning("Masukkan angka dulu!")

except Exception as e:
    st.error(f"Sistem Error: {e}")
