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
st.set_page_config(page_title="RIZKY RNG SMART SYSTEM", page_icon="🎯", layout="wide")

# CSS Premium Dark Gold
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1a1a1a; border-radius: 5px; padding: 10px 20px; color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black; }
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
        # Bersihkan data: ambil kolom angka (indeks 2)
        df['Angka'] = df.iloc[:, 2].astype(str).str.strip()
        df['Panjang'] = df['Angka'].apply(len)
    else:
        df = pd.DataFrame(columns=["Tanggal", "Sesi", "Angka", "Panjang"])

    st.title("🎯 RIZKY SMART RNG V4.5")
    st.write(f"Database aktif: **{len(df)} Sesi Tersimpan**")

    tab1, tab2, tab3, tab4 = st.tabs(["📥 INPUT DATA", "📊 ANALISIS", "🔮 PREDIKSI", "🎲 BBFS"])

    # --- TAB 1: INPUT ---
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            with st.form("input_form", clear_on_submit=True):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam")
                val_angka = st.text_input("Hasil Angka (2D-5D)")
                if st.form_submit_button("SIMPAN"):
                    if val_angka.isdigit():
                        sheet.append_row([str(tgl), jam, val_angka])
                        st.success(f"Berhasil simpan {len(val_angka)}D: {val_angka}")
                        st.rerun()
                    else: st.error("Input harus angka!")
        with c2:
            st.write("10 Data Terakhir:")
            st.dataframe(df[['Tanggal', 'Sesi', 'Angka']].tail(10), use_container_width=True)

    # --- TAB 2: ANALISIS ---
    with tab2:
        if not df.empty:
            st.subheader("Frekuensi Angka Terakhir (Ekor)")
            # Mengambil digit terakhir dari setiap input
            ekor_list = [a[-1] for a in df['Angka'] if a]
            counts = pd.Series(ekor_list).value_counts().reindex([str(i) for i in range(10)], fill_value=0)
            fig = px.bar(x=counts.index, y=counts.values, color=counts.values, color_continuous_scale='YlOrBr')
            st.plotly_chart(fig, use_container_width=True)

    # --- TAB 3: PREDIKSI (SMART FILTER) ---
    with tab3:
        st.subheader("🔮 Generator Prediksi Pintar")
        mode = st.selectbox("Pilih Target Prediksi:", ["2D", "3D", "4D", "5D"])
        jml_m = st.number_input("Jumlah Urutan (10-120):", min_value=1, value=25)
        
        if st.button("RACIK ANGKA"):
            target_len = int(mode[0])
            # FILTER DATA: Cari data yang panjangnya sama atau lebih besar
            valid_data = df[df['Panjang'] >= target_len]
            
            # Ambil angka "Hot" dari posisi ekor
            if not df.empty:
                hot_ekor = pd.Series([a[-1] for a in df['Angka']]).mode()[0]
            else:
                hot_ekor = str(random.randint(0,9))
            
            hasil_final = []
            for _ in range(jml_m):
                # Racikan: (Angka Acak) + (Hot Ekor)
                prefix = "".join([str(random.randint(0,9)) for _ in range(target_len - 1)])
                hasil_final.append(prefix + hot_ekor)
            
            st.markdown(f"### 🔥 Hasil {jml_m} Urutan {mode} Terbaik:")
            st.code(", ".join(list(set(hasil_final))))
            st.caption(f"Analisis berdasarkan Ekor terkuat: {hot_ekor}")

    # --- TAB 4: BBFS ---
    with tab4:
        st.subheader("🎲 BBFS Generator")
        bbfs_in = st.text_input("Masukkan Angka Main")
        bbfs_jml = st.number_input("Jumlah Baris:", min_value=1, value=25)
        if st.button("GENERATE"):
            if bbfs_in:
                combos = [''.join(p) for p in itertools.permutations(bbfs_in, len(bbfs_in))]
                res = random.sample(combos, min(len(combos), bbfs_jml))
                st.code(", ".join(res))

except Exception as e:
    st.error(f"Koneksi sedang dimuat... Silakan refresh jika lama. Pesan: {e}")
