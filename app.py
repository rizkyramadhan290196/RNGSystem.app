import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. KONFIGURASI TAMPILAN APP ---
st.set_page_config(
    page_title="RIZKY RNG ULTIMATE", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS CUSTOM
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KONEKSI DATABASE ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    with open(NAMA_KUNCI) as f:
        info_kunci = json.load(f)
    creds = Credentials.from_service_account_info(info_kunci, scopes=scope)
    return gspread.authorize(creds).open("Database_RNG_Rizky").get_worksheet(0)

# --- 3. LOGIKA UTAMA ---
try:
    sheet = init_connection()
    all_data = sheet.get_all_values()
    
    if len(all_data) > 1:
        df = pd.DataFrame(all_data[1:], columns=all_data[0])
        df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.strip()
    else:
        df = pd.DataFrame()

    st.title("🎯 RIZKY RNG PRO V4")

    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATABASE", "📈 GRAFIK", "🔮 PREDIKSI PRO", "🎲 BBFS"])

    # --- TAB 1 & 2 (Tetap Sama) ---
    with tab1:
        col_in, col_hist = st.columns([1, 2])
        with col_in:
            st.subheader("Input Sesi")
            with st.form("form_v4", clear_on_submit=True):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi (Jam)")
                angka = st.text_input("Hasil (4D)")
                if st.form_submit_button("SIMPAN DATA"):
                    if jam and angka:
                        sheet.append_row([str(tgl), jam, angka])
                        st.success("Tersimpan!")
                        st.rerun()
        with col_hist:
            if not df.empty:
                st.subheader("Riwayat")
                st.dataframe(df.tail(10), use_container_width=True)

    with tab2:
        if not df.empty:
            st.subheader("Statistik Digit Terakhir")
            digits = df.iloc[:, 2].str[-1].tolist()
            counts = pd.Series(digits).value_counts().reindex([str(i) for i in range(10)], fill_value=0)
            fig = px.bar(x=counts.index, y=counts.values, color=counts.values, color_continuous_scale='Goldenrod')
            st.plotly_chart(fig, use_container_width=True)

    # --- TAB 3: PREDIKSI DENGAN JUMLAH MANUAL (UPDATE!) ---
    with tab3:
        st.subheader("🔮 Generator Prediksi Multi-Urutan")
        c_tipe, c_jml = st.columns(2)
        tipe = c_tipe.selectbox("Pilih Dimensi:", ["2D", "3D", "4D", "5D"])
        # FITUR MANUAL SESUAI PERMINTAAN RIZKY
        jml_pred = c_jml.number_input("Jumlah Urutan Prediksi:", min_value=1, max_value=120, value=25)
        
        if st.button("MULAI RACIK PREDIKSI"):
            if not df.empty:
                hot_digit = df.iloc[:, 2].str[-1].mode()[0]
                
                def generate_list(n_dim, count):
                    preds = []
                    for _ in range(count):
                        # Gabungan RNG dan Hot Digit
                        prefix = "".join([str(random.randint(0,9)) for _ in range(int(n_dim[0])-1)])
                        preds.append(prefix + hot_digit)
                    return list(set(preds)) # Hilangkan duplikat

                hasil_preds = generate_list(tipe, jml_pred)
                
                st.markdown(f"### 🔥 {len(hasil_preds)} Prediksi {tipe} Terbaik:")
                st.code(", ".join(hasil_preds))
                st.info(f"Basis Data: Angka Hot Ekor ({hot_digit})")
            else:
                st.warning("Input data dulu di Tab Database!")

    # --- TAB 4: BBFS (Tetap Sama) ---
    with tab4:
        st.subheader("🎲 BBFS Smart")
        input_angka = st.text_input("Angka Main")
        jml_bbfs = st.number_input("Jumlah Urutan BBFS:", min_value=1, max_value=500, value=25)
        if st.button("GENERATE BBFS"):
            if input_angka:
                combos = list(set([''.join(p) for p in itertools.permutations(input_angka, len(input_angka))]))
                hasil = random.sample(combos, min(len(combos), jml_bbfs))
                st.code(", ".join(hasil))

except Exception as e:
    st.info("Menunggu data...")
