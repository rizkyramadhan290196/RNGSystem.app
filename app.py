import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="RIZKY V11.5 - TREND POSITION", page_icon="🎯", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #00FFFF; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 16px; font-weight: bold; }
    .slot-box { background: #000d1a; border: 1px solid #00FFFF; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .slot-title { color: #00FFFF; font-weight: bold; border-bottom: 1px solid #333; margin-bottom: 8px; font-size: 14px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #00FFFF; background-color: #001a33; color: white; }
    .autopick-box { background: linear-gradient(180deg, #001a33, #000000); border: 2px solid #00FFFF; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC V11.5 (POSITIONAL TRACKER) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except: return None

def rumus_v11_5(res_str):
    """Rumus Position: Mengunci Ekor & Melompat ke Kepala Baru"""
    try:
        n = [int(d) for d in str(res_str) if d.isdigit()]
        if len(n) >= 5:
            # Mengunci angka resonansi (1) tapi mencari pasangan baru
            v1 = (n[0] + n[4]) % 10 # AS + EKOR
            v2 = (n[1] + n[3]) % 10 # KOP + KEPALA
            v3 = (n[2] + 5) % 10    # TENGAH + MISTIK
            return f"{v1}{v2}{v3}{v1}{v2}"
        return "84184"
    except: return "84184"

def generate_pool_v11_5(invest_str, bom_str, history_str):
    # Ambil history lebih pendek (-25) agar fokus pada trend terakhir (11)
    short_hist = history_str[-25:]
    pool = list(invest_str) * 5 + list(bom_str) * 8 + list(short_hist) * 4
    
    # Tambahkan Indeks khusus untuk angka 1 (Indeks 1 = 6)
    if '1' in history_str[-5:]:
        pool.extend(['6', '6', '0', '0']) # 6 adalah indeks 1, 0 adalah mistik 1
        
    return [c for c in pool if c.isdigit()]

db = init_conn()

# --- 3. UI ---
if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATA", "📊 RADAR", "🎯 SNIPER AI", "🔄 BBFS"])
    ws = db.worksheet("5D"); df = pd.DataFrame(ws.get_all_records())

    with tab1:
        a_in = st.text_input("Input Result Terakhir (75911):")
        if st.button("💾 SIMPAN"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Data Lock!"); st.rerun()

    with tab2:
        if not df.empty:
            df['Ekor'] = df['Angka'].apply(lambda x: int(str(x)[-1:]) if len(str(x))>=1 else 0)
            st.line_chart(df['Ekor'].tail(25))
            st.write("Analisis: Ekor 1 bertahan 2x. Waspada patah arus!")

    with tab3:
        st.subheader("🎯 Sniper AI V11.5 - Position Mode")
        t_digit = st.selectbox("Pilih Digit:", [5, 4, 3, 2], index=0)
        
        if not df.empty:
            res_akhir = str(df['Angka'].iloc[-1])
            bom_v11 = rumus_v11_5(res_akhir)[:t_digit]
            hist_str = "".join(df['Angka'].astype(str).tolist())
            
            # Investasi diambil dari perpaduan history dan angka mistik
            r1 = "61" if t_digit == 2 else "".join(random.sample(hist_str, t_digit))
            r2 = "01" if t_digit == 2 else "".join(random.sample(hist_str, t_digit))
            
            st.markdown(f'<div style="text-align:center; color:#00FFFF;">🔥 BOM TRI: {bom_v11} | 🛡️ RESONANSI: {r1}-{r2}</div>', unsafe_allow_html=True)
            
            pool = generate_pool_v11_5(r1+r2, bom_v11, hist_str)
            all_gen = []
            for i in range(1, 4):
                snips = []
                w = 4 if i == 3 else 1 # Slot 3 Power ditingkatkan jadi 4x
                while len(snips) < 10:
                    random.shuffle(pool); res = "".join(pool[:t_digit])
                    if res not in snips:
                        snips.append(res)
                        for _ in range(w): all_gen.append(res)
                
                st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                grid = '<div class="grid-container">'
                for n in snips: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div></div>'
                st.markdown(grid, unsafe_allow_html=True)

            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            top5 = [x[0] for x in Counter(all_gen).most_common(5)]
            st.markdown(f"### ⚡ TOP 5 SNIPER: {' | '.join([f'🎯 {x}' for x in top5])}")
            st.markdown('</div>', unsafe_allow_html=True)
