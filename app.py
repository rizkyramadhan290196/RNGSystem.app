import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG & STYLING V11.8 ---
st.set_page_config(page_title="RIZKY V11.8 - MIRROR PREDATOR", page_icon="🦖", layout="wide")

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
    .grid-item { background: #000; border: 1px solid #FF4B4B; border-radius: 5px; padding: 12px; text-align: center; color: #FFFFFF; font-family: monospace; font-size: 18px; font-weight: bold; }
    .slot-box { background: #0d0000; border: 2px solid #FF4B4B; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; background-color: #330000; color: white; }
    .autopick-box { background: linear-gradient(180deg, #440000, #000000); border: 2px solid #FF4B4B; padding: 20px; border-radius: 15px; color: white; text-align: center; }
    .mirror-badge { background-color: #FF4B4B; color: white; padding: 2px 5px; border-radius: 3px; font-size: 10px; margin-left: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC V11.8 (MIRROR & SEED) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except: return None

def get_mirror(digit_str):
    """Fungsi Anti-Meleset: Mengubah angka ke lawannya (Indeks)"""
    kamus = {'0':'5', '1':'6', '2':'7', '3':'8', '4':'9', 
             '5':'0', '6':'1', '7':'2', '8':'3', '9':'4'}
    return "".join([kamus[d] for d in digit_str])

def predator_logic(history_list):
    if len(history_list) < 2: return list("0123456789")
    last_res = str(history_list[-1])
    last_digits = [int(d) for d in last_res if d.isdigit()]
    evens = len([d for d in last_digits if d % 2 == 0])
    odds = len([d for d in last_digits if d % 2 != 0])
    
    pool = list("0123456789")
    # Booster Angka Panas & Hantu (4, 6, 0, 9, 2)
    pool.extend(["4", "9", "6", "0", "2"] * 6)
    
    if odds >= 4: pool.extend(["0", "2", "4", "6", "8"] * 3)
    if evens >= 3: pool.extend(["1", "3", "5", "7", "9"] * 3)
    return pool

db = init_conn()

# --- 3. UI V11.8 ---
if db:
    tab1, tab2, tab3 = st.tabs(["📥 DATA INPUT", "📊 RADAR TREND", "🎯 SNIPER MASTER V11.8"])
    ws = db.worksheet("5D")
    df = pd.DataFrame(ws.get_all_records())

    with tab1:
        st.subheader("Input Result Terakhir")
        a_in = st.text_input("Masukan 5 Angka (Contoh: 79690):")
        if st.button("💾 UPDATE DATA & SINKRON"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Sistem V11.8 Berhasil Sinkron!"); st.rerun()

    with tab2:
        if not df.empty:
            df['Last2'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else 0)
            st.line_chart(df['Last2'].tail(25))
            st.info("V11.8 Analisis: Mendeteksi peralihan angka Index setelah result 690.")

    with tab3:
        st.subheader("🦖 Master Sniper V11.8 - Mirror Logic")
        t_digit = st.selectbox("Pilih Target JP:", [5, 4, 3, 2], index=0)
        
        if not df.empty:
            hist_list = df['Angka'].tolist()
            res_akhir = str(hist_list[-1])
            
            # SEEDING: Mengunci angka agar tidak berubah saat ganti digit
            random.seed(res_akhir)
            pool = predator_logic(hist_list)
            
            # 1. GENERATE MASTER ASLI
            master_raw = []
            while len(master_raw) < 15:
                random.shuffle(pool)
                res_5d = "".join(pool[:5])
                if res_5d not in master_raw:
                    master_raw.append(res_5d)
            
            # 2. GENERATE MIRROR (Angka Bayangan)
            final_master = []
            for line in master_raw:
                final_master.append(line)           # Angka Asli
                final_master.append(get_mirror(line)) # Angka Mirror
            
            # 3. SLICING
            snips_final = [line[-t_digit:] for line in final_master]

            # Tampilan SLOT #1
            st.markdown('<div class="slot-box"><div class="slot-title">🔥 SLOT #1 (ASLI & MIRROR)</div>', unsafe_allow_html=True)
            grid = '<div class="grid-container">'
            for n in snips_final[:20]:
                grid += f'<div class="grid-item">{n}</div>'
            grid += '</div></div>'
            st.markdown(grid, unsafe_allow_html=True)

            # TOP 5 PREDATOR
            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            top5 = snips_final[:5]
            st.markdown(f"### ⚡ TOP 5 PREDATOR V11.8: {' | '.join([f'🎯 {x}' for x in top5])}")
            st.markdown(f"<p style='font-size:12px;'>Berdasarkan Seed: {res_akhir}. Mengaktifkan Perlindungan Indeks (Mirroring) Otomatis.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
