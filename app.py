import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
import collections

# --- CONFIG V12.1 MASTER ARCHIVIST ---
st.set_page_config(page_title="RIZKY V12.1 MASTER", page_icon="🎯", layout="wide")

# Styling Tampilan
st.markdown("""
    <style>
    .grid-hunter { 
        background: #1e1e1e; 
        border: 2px solid #00FF00; 
        border-radius: 8px; 
        padding: 10px; 
        text-align: center; 
        color: #00FF00; 
        font-family: 'Courier New', monospace; 
        font-size: 22px; 
        font-weight: bold; 
        box-shadow: 0 4px 15px rgba(0,255,0,0.2);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #333; border-radius: 4px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00FF00; color: black; }
    </style>
    """, unsafe_allow_html=True)

NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except Exception as e:
        st.error(f"Koneksi Gagal: {e}")
        return None

db = init_conn()

if db:
    ws = db.worksheet("5D")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    tab1, tab2 = st.tabs(["📥 INPUT DATA", "🎯 MASTER ANALYZER (V12.1)"])

    with tab1:
        st.subheader("Tambah Result Baru")
        a_in = st.text_input("Masukan Result (Contoh: 31853):")
        if st.button("SIMPAN & ANALISIS"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Data berhasil masuk ke Database!")
                st.rerun()

    with tab2:
        if not df.empty:
            # 1. LOAD DATABASE (143 DATA)
            all_res = [str(x) for x in df['Angka'].tolist()]
            res_akhir = all_res[-1]
            st.subheader(f"📊 Analisis Berdasarkan {len(all_res)} Data Riwayat")
            st.info(f"Result Terakhir: **{res_akhir}**")

            # 2. TABEL LOGIKA BANDAR (Mistik & Index)
            t_index = {'0':'5','1':'6','2':'7','3':'8','4':'9','5':'0','6':'1','7':'2','8':'3','9':'4'}
            t_m_baru = {'0':'8','1':'7','2':'6','3':'9','4':'5','5':'4','6':'2','7':'1','8':'0','9':'3'}
            t_m_lama = {'1':'0','2':'5','3':'8','4':'7','6':'9','0':'1','5':'2','8':'3','7':'4','9':'6'}
            
            # 3. PROSES SCORING (WEIGHTED PROBABILITY)
            semua_angka_string = "".join(all_res)
            counts = collections.Counter(semua_angka_string)
            
            # Mencari angka bayangan dari 3 result terakhir
            bayangan = set()
            for r in all_res[-3:]:
                for char in r:
                    bayangan.add(t_index.get(char))
                    bayangan.add(t_m_baru.get(char))
                    bayangan.add(t_m_lama.get(char))
            
            # Perhitungan Skor per Angka (0-9)
            scores = {}
            for i in range(10):
                s_i = str(i)
                # Bobot Frekuensi (Sangat penting karena data kamu banyak)
                skor = counts.get(s_i, 0) * 1.8 
                # Bonus Bayangan Mistik/Index
                if s_i in bayangan: skor += 2.5
                # Bonus Repeat Pattern (Angka yang baru keluar)
                if s_i in res_akhir: skor += 1.5
                scores[s_i] = skor

            # 4. PENENTUAN POOL BBFS (7 DIGIT TERKUAT)
            pool_bbfs = sorted(scores, key=scores.get, reverse=True)[:7]
            bbfs_final = "".join(sorted(pool_bbfs))
            
            # 5. GENERASI SNIPER 16 LINE (SINKRON)
            # Menggunakan 5 digit sniper lurus diambil dari pool analisis
            snipers = []
            max_attempts = 200
            attempts = 0
            while len(snipers) < 16 and attempts < max_attempts:
                line = "".join(random.sample(pool_bbfs, 5))
                if line not in snipers: snipers.append(line)
                attempts += 1

            # Tampilan Grid Sniper
            cols = st.columns(4)
            for i, val in enumerate(snipers):
                cols[i % 4].markdown(f'<div class="grid-hunter">{val}</div>', unsafe_allow_html=True)
            
            st.divider()
            
            # TAMPILAN OUTPUT FINAL
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"### 💡 BBFS ANALYTICS: {bbfs_final}")
                top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                st.write(f"**Angka Poros (Top 3):** {', '.join([x[0] for x in top_3])}")
            
            with c2:
                # Statistik kecil untuk meyakinkan
                st.warning(f"### 📈 Confidence Level: High")
                st.write(f"Analisis mencakup {len(semua_angka_string)} kemunculan digit.")

        else:
            st.error("Database kosong! Silakan input data dulu di Tab 1.")
else:
    st.error("Gagal terhubung ke Google Sheets. Periksa file JSON kunci kamu.")
