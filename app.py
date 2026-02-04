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
    page_title="RIZKY RNG PRO V4", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS CUSTOM: Tema Midnight Gold & Sembunyikan Menu Browser
st.markdown("""
    <style>
    /* Warna Dasar */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Menghilangkan Menu Streamlit agar mirip App Asli */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Gaya Tombol */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black;
        font-weight: bold;
        border: none;
    }
    
    /* Gaya Input */
    div[data-baseweb="input"] {
        background-color: #1a1a1a !important;
        border-radius: 10px !important;
    }
    
    /* Gaya Card/Metric */
    [data-testid="stMetricValue"] { color: #FFD700 !important; }
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

def get_bbfs_smart(digits, limit):
    if not digits: return []
    all_combos = list(set([''.join(p) for p in itertools.permutations(digits, len(digits))]))
    limit = min(int(limit), len(all_combos))
    return random.sample(all_combos, limit)

# --- 3. LOGIKA UTAMA ---
try:
    sheet = init_connection()
    all_data = sheet.get_all_values()
    
    if len(all_data) > 1:
        df = pd.DataFrame(all_data[1:], columns=all_data[0])
        df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.strip()
    else:
        df = pd.DataFrame()

    st.title("🎯 RIZKY RNG PRO")
    st.caption("Sistem Analisis & Prediksi Angka Terpadu")

    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATABASE", "📈 GRAFIK", "🔮 PREDIKSI", "🎲 BBFS"])

    # --- TAB 1: DATABASE ---
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("Input Baru")
            with st.form("form_v4", clear_on_submit=True):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi (Jam)")
                angka = st.text_input("Hasil (4D)")
                if st.form_submit_button("SIMPAN DATA"):
                    if jam and angka:
                        sheet.append_row([str(tgl), jam, angka])
                        st.success("Tersimpan!")
                        st.rerun()
        with c2:
            st.subheader("Riwayat Terakhir")
            if not df.empty:
                st.dataframe(df.tail(15), use_container_width=True)
                # Fitur Download (Seperti App Pro)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Semua Data", csv, "riwayat_rizky.csv", "text/csv")

    # --- TAB 2: ANALISIS GRAFIK ---
    with tab2:
        if not df.empty:
            st.subheader("Visualisasi Statistik")
            digits = df.iloc[:, 2].str[-1].tolist()
            counts = pd.Series(digits).value_counts().reindex([str(i) for i in range(10)], fill_value=0)
            
            fig = px.bar(x=counts.index, y=counts.values, 
                         labels={'x':'Angka Ekor', 'y':'Jumlah Keluar'},
                         color=counts.values, color_continuous_scale='Goldenrod')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)
            
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("HOT (Ekor)", counts.idxmax())
            sc2.metric("COLD (Ekor)", counts.idxmin())
            sc3.metric("TOTAL SESI", len(df))

    # --- TAB 3: PREDIKSI MULTI-D ---
    with tab3:
        st.subheader("🔮 Generator Prediksi")
        tipe = st.radio("Pilih Dimensi:", ["2D", "3D", "4D", "5D"], horizontal=True)
        
        if not df.empty:
            hot_digit = df.iloc[:, 2].str[-1].mode()[0]
            if st.button("RUMUS ULANG"): st.rerun()
            
            def generate(n):
                return "".join([str(random.randint(0,9)) for _ in range(n-1)]) + hot_digit
            
            hasil_prediksi = generate(int(tipe[0]))
            st.markdown(f"""
                <div style="background:#1a1a1a; padding:20px; border-radius:15px; border-left: 5px solid #FFD700; text-align:center;">
                    <h1 style="color:#FFD700; font-size:60px;">{hasil_prediksi}</h1>
                    <p>Rumus: Hot Ekor ({hot_digit}) + RNG System</p>
                </div>
            """, unsafe_allow_html=True)

    # --- TAB 4: BBFS MANUAL ---
    with tab4:
        st.subheader("🎲 BBFS Smart")
        input_angka = st.text_input("Angka Main (Contoh: 01458)")
        jml = st.number_input("Jumlah Urutan Yang Dibutuhkan:", min_value=1, value=25)
        
        if st.button("GENERATE BBFS"):
            if input_angka:
                hasil_list = get_bbfs_smart(input_angka, jml)
                st.write(f"Berikut **{len(hasil_list)}** urutan terbaik:")
                st.code(", ".join(hasil_list))
                st.caption("Klik dua kali pada angka di atas untuk menyalin")

except Exception as e:
    st.info("Sistem sedang sinkronisasi data...")
