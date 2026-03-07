import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random

# --- CONFIG V11.9.2 ---
st.set_page_config(page_title="RIZKY V11.9.2 - BALANCE MODE", page_icon="🦖", layout="wide")

st.markdown("""
    <style>
    .grid-normal { background: #000; border: 1px solid #00FF00; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 20px; font-weight: bold; }
    .grid-twin { background: #001a00; border: 1px solid #FF00FF; border-radius: 5px; padding: 10px; text-align: center; color: #FF00FF; font-family: monospace; font-size: 20px; font-weight: bold; }
    .slot-box { background: #000500; border: 2px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 20px; }
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
    
    tab1, tab2, tab3 = st.tabs(["📥 DATA INPUT", "📊 TREND", "🎯 SNIPER V11.9.2"])

    with tab1:
        st.subheader("Update Database Rizky")
        a_in = st.text_input("Masukan Result Terakhir (30287):")
        if st.button("SINKRONKAN SISTEM"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Sistem Sinkron!")
                st.rerun()

    with tab2:
        if not df.empty:
            df['Ekor'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else int(x))
            st.line_chart(df['Ekor'].tail(20))

    with tab3:
        if not df.empty:
            res_akhir = str(df['Angka'].tolist()[-1])
            st.subheader(f"🎯 Sniper Balance (Seed: {res_akhir})")
            
            # --- LOGIKA ADAPTIVE V11.9.2 ---
            random.seed(res_akhir)
            pool_normal = list("0123456789") + list(res_akhir)*5 + list(get_mirror(res_akhir))*3
            pool_twin = list(res_akhir) * 10 + list(get_mirror(res_akhir)) * 5
            
            snipers = []
            # 10 Baris Normal (Warna Hijau)
            for _ in range(10):
                random.shuffle(pool_normal)
                snipers.append(("".join(pool_normal[:5]), "grid-normal"))
            
            # 6 Baris Twin (Warna Pink/Ungu untuk Penanda)
            for _ in range(6):
                random.shuffle(pool_twin)
                pick = random.choice(list(res_akhir))
                line = pick + pick + "".join(random.sample(pool_twin, 3))
                snipers.append((line, "grid-twin"))

            cols = st.columns(4)
            for i, (val, style) in enumerate(snipers):
                cols[i % 4].markdown(f'<div class="{style}">{val}</div>', unsafe_allow_html=True)
            
            # --- BBFS TERKUAT ---
            # Mengambil 5 digit paling sering muncul/dominan
            bbfs_pool = list(set(list(res_akhir) + list(get_mirror(res_akhir)) + ["3", "8"]))
            bbfs_final = "".join(random.sample(bbfs_pool, 6)) # Kita upgrade jadi 6 digit biar lebih aman
            st.warning(f"💡 **Rekomendasi BBFS 6 Digit (Jaga-jaga): {bbfs_final}**")
