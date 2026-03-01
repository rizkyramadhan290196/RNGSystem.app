import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG & STYLING V11.6 ---
st.set_page_config(page_title="RIZKY V11.6 - THE PREDATOR", page_icon="🦖", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #FF4B4B; border-radius: 5px; padding: 10px; text-align: center; color: #FFFFFF; font-family: monospace; font-size: 16px; font-weight: bold; }
    .slot-box { background: #0d0000; border: 1px solid #FF4B4B; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; background-color: #330000; color: white; }
    .autopick-box { background: linear-gradient(180deg, #330000, #000000); border: 2px solid #FF4B4B; padding: 20px; border-radius: 15px; color: white; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC V11.6 (ODD-EVEN BALANCE) ---
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
    """Mendeteksi Ketimpangan Ganjil/Genap & Twin Mirroring"""
    if len(history_list) < 2: return list("0123456789")
    
    last_res = str(history_list[-1])
    last_digits = [int(d) for d in last_res if d.isdigit()]
    evens = len([d for d in last_digits if d % 2 == 0])
    odds = len([d for d in last_digits if d % 2 != 0])
    
    pool = list("0123456789")
    # Jika Ganjil mendominasi (seperti 15599), tambahkan Genap ke Pool
    if odds >= 4: pool.extend(["0", "2", "4", "6", "8"] * 3)
    # Jika Genap mendominasi (seperti 11302), tambahkan Ganjil ke Pool
    if evens >= 3: pool.extend(["1", "3", "5", "7", "9"] * 3)
    
    return pool

db = init_conn()

# --- 3. UI V11.6 ---
if db:
    tab1, tab2, tab3 = st.tabs(["📥 DATA", "📊 RADAR", "🎯 SNIPER V11.6"])
    ws = db.worksheet("5D"); df = pd.DataFrame(ws.get_all_records())

    with tab1:
        a_in = st.text_input("Input Result Terakhir (11302):")
        if st.button("💾 SIMPAN DATA"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Data Predator Terkunci!"); st.rerun()

    with tab2:
        if not df.empty:
            df['Last2'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else 0)
            st.line_chart(df['Last2'].tail(20))
            st.info("Radar: Pergerakan dari Ganjil Ekstrim (99) ke Genap (02).")

    with tab3:
        st.subheader("🦖 Sniper Predator - V11.6 Mode")
        t_digit = st.selectbox("Pilih Digit:", [5, 4, 3, 2], index=0)
        
        if not df.empty:
            hist_list = df['Angka'].tolist()
            res_akhir = str(hist_list[-1])
            
            # Rumus Predator: Mencari celah antara Ganjil dan Genap
            pool = predator_logic(hist_list)
            
            # Tambahkan resonansi angka hantu (4) dan angka sisa (0, 2)
            pool.extend(["4", "0", "2", "3"] * 2)
            
            all_gen = []
            for i in range(1, 4):
                snips = []
                # Slot 3: Anti-Zonk Power
                boost = 5 if i == 3 else 1
                while len(snips) < 10:
                    random.shuffle(pool); res = "".join(pool[:t_digit])
                    if res not in snips:
                        snips.append(res)
                        for _ in range(boost): all_gen.append(res)
                
                st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                grid = '<div class="grid-container">'
                for n in snips: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div></div>'
                st.markdown(grid, unsafe_allow_html=True)

            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            top5 = [x[0] for x in Counter(all_gen).most_common(5)]
            st.markdown(f"### ⚡ TOP 5 PREDATOR: {' | '.join([f'🎯 {x}' for x in top5])}")
            st.markdown("<p style='font-size:12px;'>V11.6: Menyeimbangkan Ganjil/Genap pasca loncatan ekstrim.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
