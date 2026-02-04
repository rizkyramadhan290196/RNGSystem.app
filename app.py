import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- CONFIG ---
st.set_page_config(page_title="RIZKY RNG PRO V4.5", page_icon="🎯", layout="wide")

# CSS Premium Dark Gold
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black;
        font-weight: bold;
    }
    /* Gaya Tombol Hapus */
    .btn-hapus > div > button {
        background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    with open(NAMA_KUNCI) as f:
        info_kunci = json.load(f)
    creds = Credentials.from_service_account_info(info_kunci, scopes=scope)
    return gspread.authorize(creds).open("Database_RNG_Rizky").get_worksheet(0)

try:
    sheet = init_connection()
    all_data = sheet.get_all_values()
    
    if len(all_data) > 1:
        df = pd.DataFrame(all_data[1:], columns=all_data[0])
        df['Angka'] = df['Angka'].astype(str).str.strip()
        data_tersedia = True
    else:
        df = pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
        data_tersedia = False

    st.title("🎯 RIZKY SMART RNG V4.5")

    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATABASE", "📈 GRAFIK", "🔮 PREDIKSI PRO", "🎲 BBFS"])

    # --- TAB 1: DATABASE & HAPUS ---
    with tab1:
        c_in, c_hi = st.columns([1, 2])
        with c_in:
            st.subheader("Input Sesi")
            with st.form("form_v4", clear_on_submit=True):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Jam (Contoh: 23.00)")
                angka_in = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if jam and angka_in:
                        sheet.append_row([str(tgl), jam, str(angka_in)])
                        st.success("Berhasil! Refresh halaman.")
                        st.rerun()
            
            # FITUR HAPUS DATA (TAMBAHAN RIZKY)
            st.markdown("---")
            st.subheader("Pengaturan Data")
            if data_tersedia:
                if st.button("🗑️ HAPUS DATA TERAKHIR"):
                    # Menghapus baris terakhir di Sheets
                    total_baris = len(all_data)
                    sheet.delete_rows(total_baris)
                    st.warning("Data terakhir telah dihapus!")
                    st.rerun()
                
                # Gunakan st.columns untuk tombol reset agar tidak sengaja terpencet
                st.write("")
                with st.container():
                    st.markdown('<div class="btn-hapus">', unsafe_allow_html=True)
                    if st.checkbox("Konfirmasi Reset Semua"):
                        if st.button("🔥 RESET TOTAL DATABASE"):
                            # Menghapus semua baris kecuali judul
                            sheet.delete_rows(2, len(all_data))
                            st.error("Semua data telah dibersihkan!")
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Belum ada data untuk dihapus.")

        with c_hi:
            st.subheader("Riwayat Terakhir")
            if data_tersedia:
                st.table(df.tail(10))
            else:
                st.info("Database kosong.")

    # --- TAB 3: PREDIKSI ---
    with tab3:
        st.subheader("🔮 Generator Prediksi")
        if data_tersedia:
            col_t, col_j = st.columns(2)
            mode = col_t.selectbox("Pilih Target:", ["2D", "3D", "4D", "5D"])
            jml_m = col_j.number_input("Jumlah Urutan:", min_value=1, max_value=120, value=25)
            
            if st.button("MULAI RACIK"):
                hot_ekor = df['Angka'].str[-1].mode()[0] if not df.empty else "7"
                hasil_final = []
                for _ in range(int(jml_m)):
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    hasil_final.append(prefix + hot_ekor)
                st.code(", ".join(list(set(hasil_final))))
                st.success(f"Berhasil meracik berdasarkan Ekor: {hot_ekor}")
        else:
            st.warning("Input data dulu di Tab DATABASE!")

    # --- TAB 4: BBFS ---
    with tab4:
        st.subheader("🎲 BBFS Manual")
        b_in = st.text_input("Angka Main")
        b_jml = st.number_input("Urutan BBFS:", min_value=1, value=25)
        if st.button("GENERATE BBFS"):
            if b_in:
                combos = [''.join(p) for p in itertools.permutations(b_in, len(b_in))]
                res = random.sample(combos, min(len(combos), b_jml))
                st.code(", ".join(res))

except Exception as e:
    st.error(f"Sistem sedang sinkronisasi: {e}")
