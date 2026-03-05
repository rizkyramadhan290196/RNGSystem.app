import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random

# --- CONFIG V11.9 ---
st.set_page_config(page_title="RIZKY V11.9 - TRIPLE GUARD", page_icon="🦖", layout="wide")

st.markdown("""
    <style>
    .grid-item { background: #000; border: 1px solid #00FF00; border-radius: 5px; padding: 12px; text-align: center; color: #00FF00; font-family: monospace; font-size: 18px; font-weight: bold; }
    .slot-box { background: #001100; border: 2px solid #00FF00; padding: 15px; border-radius: 12px; }
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

def get_mirror(digit_str):
    kamus = {'0':'5', '1':'6', '2':'7', '3':'8', '4':'9', '5':'0', '6':'1', '7':'2', '8':'3', '9':'4'}
    return "".join([kamus[d] for d in digit_str])

def predator_logic_v9(history_list):
    if len(history_list) < 2: return list("0123456789")
    last_res = str(history_list[-1]) # Result 10937
    
    pool = list("0123456789")
    # BOOSTER 1: Angka Lengket (0, 9, 3, 7)
    pool.extend(list(last_res) * 5)
    # BOOSTER 2: Anti-Mirror (Indeks dari result)
    pool.extend(list(get_mirror(last_res)) * 5)
    # BOOSTER 3: Angka Hantu (4, 6)
    pool.extend(["4", "6", "2", "8"] * 3)
    
    return pool

db = init_conn()

if db:
    ws = db.worksheet("5D")
    df = pd.DataFrame(ws.get_all_records())
    
    tab1, tab2, tab3 = st.tabs(["📥 DATA INPUT", "📊 TREND", "🎯 SNIPER V11.9"])

    with tab1:
        a_in = st.text_input("Masukan Result Terakhir (10937):")
        if st.button("SINKRONKAN V11.9"):
            ws.append_row([str(datetime.now().date()), a_in])
            st.success("V11.9 Aktif!"); st.rerun()

    with tab3:
        if not df.empty:
            res_akhir = str(df['Angka'].tolist()[-1])
            random.seed(res_akhir)
            pool = predator_logic_v9(df['Angka'].tolist())
            
            master_raw = []
            while len(master_raw) < 12:
                random.shuffle(pool)
                line = "".join(pool[:5])
                if line not in master_raw:
                    master_raw.append(line)
                    master_raw.append(get_mirror(line))

            st.subheader(f"🎯 Sniper V11.9 (Seed: {res_akhir})")
            t_digit = st.selectbox("Digit:", [5,4,3,2], index=1)
            
            snips = [l[-t_digit:] for l in master_raw]
            
            st.markdown('<div class="slot-box">', unsafe_allow_html=True)
            cols = st.columns(4)
            for i, s in enumerate(snips[:20]):
                cols[i%4].markdown(f'<div class="grid-item">{s}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
