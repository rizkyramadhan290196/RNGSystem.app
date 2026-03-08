import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random

# --- CONFIG V11.9.3 "THE HUNTER" ---
st.set_page_config(page_title="RIZKY V11.9.3 - THE HUNTER", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .grid-hunter { background: #000; border: 1px solid #FFD700; border-radius: 5px; padding: 10px; text-align: center; color: #FFD700; font-family: monospace; font-size: 22px; font-weight: bold; box-shadow: 0px 0px 10px #FFD700; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0e1117; }
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

db = init_conn()

if db:
    ws = db.worksheet("5D")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    tab1, tab2, tab3 = st.tabs(["📥 DATA INPUT", "📊 TREND GAJAH", "🎯 HUNTER V11.9.3"])

    with tab1:
        a_in = st.text_input("Masukan Result Terakhir (97186):")
        if st.button("SINKRONKAN HUNTER"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Target Terkunci! Hunter Aktif.")
                st.rerun()

    with tab2:
        if not df.empty:
            st.write("Analisa Angka Gajah (Besar/Kecil)")
            df['LastDigit'] = df['Angka'].apply(lambda x: int(str(x)[-1]))
            st.bar_chart(df['LastDigit'].tail(15))

    with tab3:
        if not df.empty:
            res_akhir = str(df['Angka'].tolist()[-1])
            st.subheader(f"🎯 Sniper Hunter (Target: {res_akhir})")
            
            # --- LOGIKA HUNTER V11.9.3 ---
            random.seed(res_akhir)
            # Pool Angka Gajah + Mirror Otomatis
            pool = list(res_akhir) * 10 
            pool.extend(list(get_mirror(res_akhir)) * 8)
            pool.extend(["4", "9", "2", "7", "0"] * 4) # Angka rawan JP
            
            hunters = []
            while len(hunters) < 16:
                random.shuffle(pool)
                line = "".join(pool[:5])
                if line not in hunters: hunters.append(line)

            cols = st.columns(4)
            for i, val in enumerate(hunters):
                cols[i % 4].markdown(f'<div class="grid-hunter">{val}</div>', unsafe_allow_html=True)
            
            # --- BBFS HUNTER (6 DIGIT) ---
            bbfs_list = list(set(list(res_akhir) + ["4", "9", "2"]))
            bbfs_final = "".join(random.sample(bbfs_list, 6))
            st.warning(f"💡 **BBFS HUNTER (6 DIGIT): {bbfs_final}**")
