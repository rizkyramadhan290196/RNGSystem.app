import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. KONFIGURASI PASSWORD ---
# Ganti "1234" dengan password keinginan kamu
PASSWORD_RAHASIA = "rizky77" 

# --- CONFIG TAMPILAN ---
st.set_page_config(page_title="RIZKY RNG PRO V4.5", page_icon="🎯", layout="wide")

# CSS Premium
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
    .btn-hapus > div > button {
        background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI LOGIN ---
def check_password():
    """Returns True if the user had the correct password."""
    if "password_correct" not in st.session_state:
        # Tampilan Login
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>🔓 AKSES TERKUNCI</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukkan Kode Akses Rizky:", type="password")
        if st.button("MASUK SISTEM"):
            if pwd == PASSWORD_RAHASIA:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Kode Salah! Akses Ditolak.")
        return False
    return True

# --- CEK LOGIN DULU ---
if check_password():

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
        
        # Tombol Logout kecil di pojok
        if st.sidebar.button("Log Out / Kunci"):
            del st.session_state["password_correct"]
            st.rerun()

        tab1, tab2, tab3, tab4 = st.tabs(["📥 DATABASE", "📈 GRAFIK", "🔮 PREDIKSI PRO", "🎲 BBFS"])

        # --- TAB 1: DATABASE & HAPUS ---
        with tab1:
            c_in, c_hi = st.columns([1, 2])
            with c_in:
                st.subheader("Input Sesi")
                with st.form("form_v4", clear_on_submit=True):
                    tgl = st.date_input("Tanggal", datetime.now())
                    jam = st.text_input("Jam")
                    angka_in = st.text_input("Hasil Angka")
                    if st.form_submit_button("SIMPAN DATA"):
                        if jam and angka_in:
                            sheet.append_row([str(tgl), jam, str(angka_in)])
                            st.success("Berhasil! Refresh halaman.")
                            st.rerun()
                
                st.markdown("---")
                st.subheader("Pengaturan Data")
                if data_tersedia:
                    if st.button("🗑️ HAPUS DATA TERAKHIR"):
                        sheet.delete_rows(len(all_data))
                        st.warning("Data terakhir telah dihapus!")
                        st.rerun()
                    
                    st.write("")
                    with st.container():
                        st.markdown('<div class="btn-hapus">', unsafe_allow_html=True)
                        if st.checkbox("Konfirmasi Reset Semua"):
                            if st.button("🔥 RESET TOTAL DATABASE"):
                                sheet.delete_rows(2, len(all_data))
                                st.error("Semua data telah dibersihkan!")
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

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
                jml_m = col_j.number_input("Jumlah Urutan:", min_value=1, value=25)
                
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
