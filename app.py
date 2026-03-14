import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
import collections

# --- ENGINE V15: THE MIRROR-TRAP (ANTI-INDEX SYSTEM) ---
st.set_page_config(page_title="RIZKY V15 MIRROR-TRAP", page_icon="🪤", layout="wide")

# Styling UI Sniper
st.markdown("""
    <style>
    .grid-hunter { 
        background: #0d0d0d; 
        border: 2px solid #ff00ff; 
        border-radius: 8px; 
        padding: 12px; 
        text-align: center; 
        color: #ff00ff; 
        font-family: 'Courier New', monospace; 
        font-size: 22px; 
        font-weight: bold;
        box-shadow: 0 0 10px #ff00ff;
    }
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
    data_raw = ws.get_all_records()
    df = pd.DataFrame(data_raw)
    
    tab1, tab2 = st.tabs(["📥 INPUT DATA", "🎯 MIRROR-TRAP ANALYSIS (V15)"])

    with tab1:
        st.subheader("Input Result Baru")
        a_in = st.text_input("Masukan Result (Misal: 94140):")
        if st.button("PROSES DATA"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success(f"Result {a_in} tersimpan!")
                st.rerun()

    with tab2:
        if not df.empty:
            all_res = [str(x) for x in df['Angka'].tolist()]
            res_akhir = all_res[-1]
            
            # --- LOGIKA V15: THE MIRROR-TRAP ---
            t_idx = {'0':'5','1':'6','2':'7','3':'8','4':'9','5':'0','6':'1','7':'2','8':'3','9':'4'}
            
            # 1. HITUNG SKOR DASAR (40 Sesi Terakhir - Fokus Tren Menengah)
            raw_scores = {str(i): 0 for i in range(10)}
            target_history = all_res[-40:]
            for r in target_history:
                for char in r:
                    raw_scores[char] += 1.0

            # 2. LOGIKA PAIRING INDEX (Sistem Jaring)
            # Menghitung kekuatan pasangan (0-5, 1-6, dst)
            pair_scores = {}
            for i in range(5):
                s1, s2 = str(i), t_idx[str(i)]
                combined = raw_scores[s1] + raw_scores[s2]
                pair_scores[f"{s1}{s2}"] = combined

            # 3. FIX BBFS 6 DIGIT (3 Pasang Terkuat)
            top_pairs = sorted(pair_scores, key=pair_scores.get, reverse=True)[:3]
            bbfs_6_digit = list("".join(top_pairs))
            bbfs_final = "".join(sorted(bbfs_6_digit))

            # 4. POSITIONING ANALYSIS (10 Sesi Terakhir - Suhu Panas)
            pos = {'as':[], 'kop':[], 'kep':[], 'eko':[]}
            for r in all_res[-10:]:
                if len(r) >= 4:
                    pos['as'].append(r[-4]); pos['kop'].append(r[-3])
                    pos['kep'].append(r[-2]); pos['eko'].append(r[-1])
            
            # Ambil 2 kandidat terkuat per posisi
            best_pos = {k: [i[0] for i in collections.Counter(v).most_common(2)] for k, v in pos.items()}

            snipers = []
            # Kombinasi berdasarkan posisi
            for a in best_pos['as']:
                for k in best_pos['kop']:
                    for kp in best_pos['kep']:
                        for ek in best_pos['eko']:
                            line = f"{a}{k}{kp}{ek}"
                            # Filter: Wajib masuk dalam radar BBFS Mirror-Trap
                            if all(c in bbfs_6_digit for c in line):
                                if line not in snipers: snipers.append(line)
            
            # Jika kurang dari 10 line, isi dengan sample BBFS agar tetap 10 line
            while len(snipers) < 10:
                line = "".join(random.sample(bbfs_6_digit, 4))
                if line not in snipers: snipers.append(line)

            # --- DISPLAY INTERFACE ---
            st.subheader(f"📊 Sniper V15 (Analisis Berdasarkan {len(all_res)} Data)")
            st.write(f"Result Terakhir: **{res_akhir}**")
            
            cols = st.columns(5)
            for i, val in enumerate(snipers[:10]):
                cols[i % 5].markdown(f'<div class="grid-hunter">{val}</div>', unsafe_allow_html=True)
            
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"### 💡 BBFS MIRROR-TRAP: {bbfs_final}")
                st.caption("BBFS ini mengunci 3 pasang angka Index terkuat.")
            with c2:
                # Menampilkan pasangan index yang dipilih
                st.warning(f"### 🎯 PAIRING AKTIF: {', '.join(top_pairs)}")
                st.caption("Sistem mendeteksi siklus bandar di angka-angka ini.")

        else:
            st.error("Database kosong. Input result dulu!")
else:
    st.error("Gagal koneksi ke Google Sheets!")
