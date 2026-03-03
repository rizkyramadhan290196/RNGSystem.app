import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG & STYLING V11.7 ---
st.set_page_config(page_title="RIZKY V11.7 - MASTER PREDATOR", page_icon="🦖", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
    .grid-item { background: #000; border: 1px solid #FF4B4B; border-radius: 5px; padding: 12px; text-align: center; color: #FFFFFF; font-family: monospace; font-size: 18px; font-weight: bold; }
    .slot-box { background: #0d0000; border: 2px solid #FF4B4B; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; background-color: #330000; color: white; }
    .autopick-box { background: linear-gradient(180deg, #440000, #000000); border: 2px solid #FF4B4B; padding: 20px; border-radius: 15px; color: white; text-align: center; }
    .info-text { color: #FF4B4B; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC V11.7 (MASTER SEED & SLICING) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except: return None

def predator_logic(history_list):
    if len(history_list) < 2: return list("0123456789")
    
    last_res = str(history_list[-1])
    last_digits = [int(d) for d in last_res if d.isdigit()]
    evens = len([d for d in last_digits if d % 2 == 0])
    odds = len([d for d in last_digits if d % 2 != 0])
    
    pool = list("0123456789")
    if odds >= 4: pool.extend(["0", "2", "4", "6", "8"] * 5)
    if evens >= 3: pool.extend(["1", "3", "5", "7", "9"] * 5)
    
    # Tambahkan Angka Hantu & Sisa dengan Bobot Lebih Berat
    pool.extend(["4", "0", "2", "3", "6"] * 4) 
    return pool

db = init_conn()

# --- 3. UI V11.7 ---
if db:
    tab1, tab2, tab3 = st.tabs(["📥 DATA INPUT", "📊 RADAR TREND", "🎯 SNIPER MASTER V11.7"])
    ws = db.worksheet("5D")
    data_all = ws.get_all_records()
    df = pd.DataFrame(data_all)

    with tab1:
        st.subheader("Input Result Bandar")
        a_in = st.text_input("Contoh (75502):")
        if st.button("💾 KUNCI DATA PREDATOR"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Data Berhasil Disinkronkan!"); st.rerun()

    with tab2:
        if not df.empty:
            df['Last2'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else 0)
            st.line_chart(df['Last2'].tail(20))
            st.markdown("<p class='info-text'>Radar: Mendeteksi Pola Balikan (Mirror) dan Angka Jenuh.</p>", unsafe_allow_html=True)

    with tab3:
        st.subheader("🦖 Master Sniper - Mode Sinkron 90%")
        t_digit = st.selectbox("Pilih Target JP:", [5, 4, 3, 2], index=0)
        
        if not df.empty:
            hist_list = df['Angka'].tolist()
            res_akhir = str(hist_list[-1])
            
            # --- KUNCI UTAMA: SEEDING ---
            # Angka Sniper tidak akan berubah-ubah selama result terakhir tetap.
            random.seed(res_akhir) 
            pool = predator_logic(hist_list)
            
            # --- GENERATE MASTER 5D (Pondasi Utama) ---
            master_lines = []
            while len(master_lines) < 30: # Kita buat 30 baris master
                random.shuffle(pool)
                res_5d = "".join(pool[:5])
                if res_5d not in master_lines:
                    master_lines.append(res_5d)
            
            # --- SLICING SYSTEM (Sinkronisasi 2D/4D/5D) ---
            # Memotong angka belakang sesuai pilihan t_digit
            snips_final = [line[-t_digit:] for line in master_lines]

            # SLOT #1 (Top 10)
            st.markdown('<div class="slot-box"><div class="slot-title">🔥 SLOT #1 (SINKRON)</div>', unsafe_allow_html=True)
            grid1 = '<div class="grid-container">'
            for n in snips_final[:10]: grid1 += f'<div class="grid-item">{n}</div>'
            grid1 += '</div></div>'
            st.markdown(grid1, unsafe_allow_html=True)

            # SLOT #2 (Pelapis)
            st.markdown('<div class="slot-box"><div class="slot-title">📡 SLOT #2 (CADANGAN)</div>', unsafe_allow_html=True)
            grid2 = '<div class="grid-container">'
            for n in snips_final[10:20]: grid2 += f'<div class="grid-item">{n}</div>'
            grid2 += '</div></div>'
            st.markdown(grid2, unsafe_allow_html=True)

            # TOP 5 PREDATOR (Berdasarkan Kalkulasi Terkuat)
            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            top5 = snips_final[:5]
            st.markdown(f"### ⚡ TOP 5 PREDATOR SINKRON: {' | '.join([f'🎯 {x}' for x in top5])}")
            st.markdown(f"<p style='font-size:12px;'>V11.7: Berdasarkan Seed Result {res_akhir}. Angka 2D & 4D terkunci pada Master 5D.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Koneksi Database Terputus. Cek file JSON!")
