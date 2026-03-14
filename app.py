import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
import collections

# --- ENGINE V14: THE SNIPER (STRICT 6-DIGIT BBFS) ---
st.set_page_config(page_title="RIZKY V14 SNIPER", page_icon="🎯", layout="wide")

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
    
    tab1, tab2 = st.tabs(["📥 INPUT", "🎯 SNIPER ANALYSIS"])

    with tab1:
        a_in = st.text_input("Masukan Result:")
        if st.button("RUN"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.rerun()

    with tab2:
        if not df.empty:
            all_res = [str(x) for x in df['Angka'].tolist()]
            res_akhir = all_res[-1]
            
            # --- LOGIKA ANALISIS POSISI (90% ACCURACY TARGET) ---
            t_idx = {'0':'5','1':'6','2':'7','3':'8','4':'9','5':'0','6':'1','7':'2','8':'3','9':'4'}
            t_mb = {'0':'8','1':'7','2':'6','3':'9','4':'5','5':'4','6':'2','7':'1','8':'0','9':'3'}
            
            scores = {str(i): 0 for i in range(10)}

            # 1. ANALISIS KEMUNCULAN (Berdasarkan Jarak 20 Sesi Terakhir)
            recent_30 = all_res[-30:]
            for i, r in enumerate(recent_30):
                weight = (i + 1) / 30
                for char in r:
                    scores[char] += weight * 3.5

            # 2. LOGIKA MISTIK & INDEX (Dari 2 Sesi Terakhir)
            shadows = set()
            for r in all_res[-2:]:
                for c in r:
                    shadows.update([t_idx.get(c), t_mb.get(c)])
            
            for s in shadows:
                if s: scores[s] += 5.0

            # 3. ELIMINASI & PENYEMPITAN (BBFS 6 DIGIT SAJA)
            # Kita hanya mengambil 6 angka dengan skor tertinggi (Top Tier)
            bbfs_6_digit = sorted(scores, key=scores.get, reverse=True)[:6]
            bbfs_final = "".join(sorted(bbfs_6_digit))

            # 4. GENERATE SNIPER 10 LINE (SANGAT KETAT)
            # Sniper dibuat dengan pola 4D yang mengambil dari 6 digit bbfs
            snipers = []
            while len(snipers) < 10:
                # Menggunakan 4 digit untuk 4D, diambil dari 6 digit BBFS
                line = "".join(random.sample(bbfs_6_digit, 4))
                if line not in snipers: snipers.append(line)

            # --- DISPLAY ---
            st.subheader(f"📊 Sniper Analysis V14 (History: {len(all_res)})")
            
            cols = st.columns(5)
            for i, val in enumerate(snipers):
                cols[i % 5].markdown(f'<div style="background: #111; border: 1px solid #00FF00; padding: 15px; text-align: center; color: #00FF00; font-size: 24px; font-weight: bold; border-radius: 5px;">{val}</div>', unsafe_allow_html=True)
            
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"### 💡 BBFS FIXED (6 DIGIT): {bbfs_final}")
            with c2:
                top_3 = sorted(scores, key=scores.get, reverse=True)[:3]
                st.warning(f"### 🎯 ANGKA POROS: {', '.join(top_3)}")
