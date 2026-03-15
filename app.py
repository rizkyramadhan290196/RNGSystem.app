import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
import collections

# --- ENGINE V16: THE GHOST HUNTER (RENOVASI TOTAL) ---
st.set_page_config(page_title="RIZKY V16 GHOST HUNTER", page_icon="👻", layout="wide")

st.markdown("""
    <style>
    .header-box { background: #1a1a1a; color: #00FF00; padding: 20px; border-radius: 10px; border: 1px solid #00FF00; text-align: center; margin-bottom: 20px; }
    .grid-5d { background: #002b36; border: 1px solid #2aa198; border-radius: 5px; padding: 10px; text-align: center; color: #2aa198; font-family: 'Courier New'; font-size: 20px; font-weight: bold; }
    .grid-4d { background: #1a1a1a; border: 1px solid #d33682; border-radius: 5px; padding: 10px; text-align: center; color: #d33682; font-family: 'Courier New'; font-size: 20px; font-weight: bold; }
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
    except: return None

db = init_conn()

if db:
    ws = db.worksheet("5D")
    df = pd.DataFrame(ws.get_all_records())
    
    tab1, tab2, tab3 = st.tabs(["📥 INPUT DATA", "🎯 5D ANALYSIS", "🎯 4D SNIPER"])

    with tab1:
        a_in = st.text_input("Masukan Result Terakhir (Contoh: 02629):")
        if st.button("UPDATE DATABASE"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Data Berhasil Disimpan!")
                st.rerun()

    if not df.empty:
        all_res = [str(x) for x in df['Angka'].tolist()]
        res_akhir = all_res[-1]
        t_idx = {'0':'5','1':'6','2':'7','3':'8','4':'9','5':'0','6':'1','7':'2','8':'3','9':'4'}

        # --- LOGIKA CORE V16 (GHOST SCORING) ---
        scores = {str(i): 0 for i in range(10)}
        for i in range(10):
            s_i = str(i)
            # Gap Analysis: Cari kapan terakhir muncul
            gap = 0
            for idx, r in enumerate(reversed(all_res)):
                if s_i in r: break
                gap += 1
            scores[s_i] = gap * 3.0 # Angka yang lama absen (seperti 8) dapat skor tinggi
        
        # Tambahkan skor untuk Index dari result terakhir (02629)
        for char in res_akhir:
            scores[t_idx[char]] += 4.5

        with tab2:
            st.markdown('<div class="header-box"><h1>🎯 5D POSITION MASTER</h1></div>', unsafe_allow_html=True)
            # Analisis Posisi 5 Digit (History 20 sesi)
            posisi = {0:[], 1:[], 2:[], 3:[], 4:[]}
            for r in all_res[-20:]:
                r_pad = r.zfill(5)
                for i in range(5): posisi[i].append(r_pad[i])
            
            # Ambil top 3 tiap posisi
            best_pos = {k: [i[0] for i in collections.Counter(v).most_common(3)] for k, v in posisi.items()}
            
            snipers_5d = []
            for _ in range(12):
                line = "".join([random.choice(best_pos[i]) for i in range(5)])
                if line not in snipers_5d: snipers_5d.append(line)
            
            cols = st.columns(4)
            for i, val in enumerate(snipers_5d):
                cols[i % 4].markdown(f'<div class="grid-5d">{val}</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="header-box"><h1>🎯 4D SNIPER KETAT</h1></div>', unsafe_allow_html=True)
            # BBFS 6 Digit paling ketat (Ghost Logic)
            top_6 = sorted(scores, key=scores.get, reverse=True)[:6]
            if '8' not in top_6: top_6[-1] = '8' # Wajib kunci angka 8
            bbfs_final = "".join(sorted(top_6))
            
            # Sniper 4D (Hanya 10 Line)
            snipers_4d = []
            while len(snipers_4d) < 10:
                line = "".join(random.sample(top_6, 4))
                if line not in snipers_4d: snipers_4d.append(line)

            cols = st.columns(5)
            for i, val in enumerate(snipers_4d):
                cols[i % 5].markdown(f'<div class="grid-4d">{val}</div>', unsafe_allow_html=True)
            
            st.divider()
            st.success(f"### 💡 BBFS 4D (GHOST SYSTEM): {bbfs_final}")
            st.warning(f"### 🎯 ANGKA GHOST (BOM): 8")

    else:
        st.error("Isi database dulu, Ky!")
else:
    st.error("Koneksi Gagal!")
