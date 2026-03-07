import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random

# --- CONFIG V11.9.1 ---
st.set_page_config(page_title="RIZKY V11.9.1 - TWIN BOOSTER", page_icon="🦖", layout="wide")

# CSS Neon Style + Better Table
st.markdown("""
    <style>
    .grid-item { background: #000; border: 1px solid #00FF00; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 20px; font-weight: bold; }
    .slot-box { background: #001100; border: 2px solid #00FF00; padding: 15px; border-radius: 12px; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border-radius: 5px; color: white; padding: 10px 20px; }
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

def predator_logic_v11_9_1(history_list):
    if len(history_list) < 1: return list("0123456789")
    last_res = str(history_list[-1]) # Misal: 05007
    
    pool = list("0123456789")
    
    # BOOSTER: Angka Lengket & Mirror (Fokus Twin)
    pool.extend(list(last_res) * 8) 
    pool.extend(list(get_mirror(last_res)) * 6)
    
    # KUNCI TWIN: Paksa angka yang baru keluar jadi pasangan kembar
    for char in last_res:
        pool.extend([char, char] * 4) 
        
    # Angka Hantu Pendamping
    pool.extend(["2", "4", "8", "6"] * 3)
    
    return pool

db = init_conn()

if db:
    ws = db.worksheet("5D")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    tab1, tab2, tab3 = st.tabs(["📥 DATA INPUT", "📊 TREND ANALYST", "🎯 SNIPER V11.9.1"])

    with tab1:
        st.subheader("Update Database Rizky")
        a_in = st.text_input("Masukan Result Terakhir (Contoh: 05007):")
        if st.button("SINKRONKAN SISTEM V11.9.1"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success(f"Result {a_in} Berhasil Disimpan! Sistem Update.")
                st.rerun()

    with tab2:
        if not df.empty:
            st.subheader("Grafik Pergerakan Angka (Trend)")
            # Ambil 2 angka belakang (ekor) untuk grafik
            df['Ekor'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else int(x))
            st.line_chart(df['Ekor'].tail(15))
            st.write("Pantau: Jika grafik mendatar, artinya bandar main angka kembar/kecil.")

    with tab3:
        if not df.empty:
            res_akhir = str(df['Angka'].tolist()[-1])
            st.subheader(f"🎯 Sniper Master (Seed: {res_akhir})")
            
            digit_opsi = st.radio("Pilih Digit:", [5, 4, 3, 2], index=1, horizontal=True)
            
            # Generate Sniper
            random.seed(res_akhir)
            pool = predator_logic_v11_9_1(df['Angka'].tolist())
            
            master_raw = []
            while len(master_raw) < 16: # Kita tambah jadi 16 baris
                random.shuffle(pool)
                line = "".join(pool[:5])
                if line not in master_raw:
                    master_raw.append(line)

            # Tampilan Grid Neon
            st.markdown('<div class="slot-box">', unsafe_allow_html=True)
            cols = st.columns(4)
            for i, val in enumerate(master_raw):
                sniper_final = val[-digit_opsi:]
                cols[i % 4].markdown(f'<div class="grid-item">{sniper_final}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # FITUR BARU: BBFS Rekomendasi
            st.info("💡 **Rekomendasi BBFS (5 Digit):**")
            bbfs_top = "".join(list(set(pool))[:5])
            st.success(f"Coba Pasang BBFS: **{bbfs_top}** (Gunakan ini jika saldo mencukupi)")
