import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random

# --- CONFIG V11.9.3 STABLE ---
st.set_page_config(page_title="RIZKY V11.9.3 HUNTER", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .grid-hunter { background: #1e1e1e; border: 2px solid #00FF00; border-radius: 8px; padding: 10px; text-align: center; color: #00FF00; font-family: 'Courier New', monospace; font-size: 20px; font-weight: bold; }
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
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    tab1, tab2 = st.tabs(["📥 INPUT", "🎯 HUNTER SNIPER"])

    with tab1:
        a_in = st.text_input("Masukan Result:")
        if st.button("RUN HUNTER"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.rerun()

    with tab2:
        if not df.empty:
            res_akhir = str(df['Angka'].tolist()[-1])
            st.subheader(f"🎯 Sniper Hunter (Target: {res_akhir})")
            
            # --- PENGAMAN DATA (Anti Error) ---
            digit_unik = list(set(list(res_akhir)))
            pool = digit_unik + ["0","1","2","3","4","5","6","7","8","9"]
            pool = list(set(pool)) # Hapus duplikat
            
            # Generasi Sniper
            snipers = []
            while len(snipers) < 16:
                line = "".join(random.sample(pool, 5))
                if line not in snipers: snipers.append(line)

            cols = st.columns(4)
            for i, val in enumerate(snipers):
                cols[i % 4].markdown(f'<div class="grid-hunter">{val}</div>', unsafe_allow_html=True)
            
            # --- PENGAMAN BBFS (Anti ValueError) ---
            # Pastikan pool punya minimal 6 angka untuk sample
            if len(pool) >= 6:
                bbfs_final = "".join(random.sample(pool, 6))
            else:
                bbfs_final = "Error: Data kurang"
            
            st.success(f"💡 BBFS HUNTER (6 DIGIT): {bbfs_final}")
