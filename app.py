import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="RIZKY V11.3 - RNG HUNTER", page_icon="📈", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 16px; font-weight: bold; }
    .slot-box { background: #001220; border: 2px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 15px; position: relative; }
    .slot-title { color: #FFD700; font-weight: bold; border-bottom: 1px solid #444; margin-bottom: 8px; font-size: 14px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; height: 3.5em; background-color: #1a1a1a; color: white; }
    .autopick-box { background: linear-gradient(45deg, #001f3f, #000000); border: 2px solid #00FF00; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-top: 20px; box-shadow: 0px 0px 15px #00FF00; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC CORE (RNG HUNTER SYSTEM) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except: return None

def hitung_triangle_rng(res_str):
    """Rumus Hunter: Mencari Titik Tengah Arus"""
    try:
        n = [int(d) for d in str(res_str) if d.isdigit()]
        if len(n) >= 5:
            v1 = (n[0] + n[3] + 2) % 10 # AS + KEPALA + OFFSET
            v2 = (n[1] + n[4] + 4) % 10 # KOP + EKOR + OFFSET
            v3 = (n[2] * 2 + 7) % 10    # TENGAH * 2 + MISTIK
            return f"{v1}{v2}{v3}{v1}"
        return "2872"
    except: return "2872"

def generate_pool_hunter(invest_str, bom_str, history_str):
    """Sistem RNG Dinamis: Fokus pada lompatan angka berikutnya"""
    # Hanya ambil 15 digit terakhir agar tidak stagnan di angka lama
    short_hist = history_str[-15:] if history_str else ""
    pool = list(invest_str) * 4 + list(bom_str) * 6 + list(short_hist) * 2
    
    # Mistik Hunter Map
    m_map = {'0':'7','1':'0','7':'0','4':'9','9':'4','5':'8','8':'5','2':'5','3':'8','6':'9'}
    for char in (invest_str + bom_str):
        if char in m_map: pool.append(m_map[char])
        
    # RNG Jumper: Tambahkan 3 angka acak murni untuk mengecoh bandar
    pool.extend([str(random.randint(0, 9)) for _ in range(3)])
    return [c for c in pool if c.isdigit()]

db = init_conn()

# --- 3. UI ---
if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V11.3 - RNG HUNTER")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK"):
        if pwd == PASSWORD_RAHASIA: st.session_state["password_correct"] = True; st.rerun()
    st.stop()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATA", "📊 ANALISIS", "🎯 SNIPER AI", "🔄 BBFS"])
    ws = db.worksheet("5D")
    df = pd.DataFrame(ws.get_all_records())

    with tab1:
        st.subheader("📥 Input Result")
        a_in = st.text_input("Input 5D:")
        if st.button("💾 SIMPAN"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success("Data Tersimpan!"); st.rerun()

    with tab2:
        st.subheader("📊 Grafik Tren Arus RNG")
        if not df.empty:
            # Ambil 2D belakang dari setiap result untuk grafik
            df['2D'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else 0)
            st.line_chart(df['2D'].tail(20)) # Tampilkan 20 result terakhir
            st.write("Interpretasi: Grafik naik (Angka Besar), Grafik turun (Angka Kecil).")

    with tab3:
        st.subheader("🎯 Sniper AI Hunter Mode")
        t_digit = st.selectbox("Digit:", [2, 3, 4, 5], index=0)
        
        if not df.empty:
            res_akhir = str(df['Angka'].iloc[-1])
            hist_full = "".join(df['Angka'].astype(str).tolist())
            
            # Triangle & Invest
            bom_tri = hitung_triangle_rng(res_akhir)[:t_digit]
            r1 = "".join(random.sample(hist_full, t_digit)) if len(hist_full) >= t_digit else "00"
            r2 = "".join(random.sample(hist_full, t_digit)) if len(hist_full) >= t_digit else "99"
            
            st.markdown(f'<div style="background:#001220; border:2px solid #00FF00; padding:15px; border-radius:10px; text-align:center; color: white;">🛡️ INVESTASI: {r1} — {r2} | 🔥 BOM TRI: {bom_tri}</div>', unsafe_allow_html=True)
            
            pool = generate_pool_hunter(r1+r2, bom_tri, hist_full)
            all_gen = []
            
            for i in range(1, 4):
                snips = []
                while len(snips) < 10:
                    random.shuffle(pool)
                    res = "".join(pool[:t_digit])
                    if res not in snips: 
                        snips.append(res)
                        # Slot 3 tetap prioritas
                        weight = 3 if i == 3 else 1
                        for _ in range(weight): all_gen.append(res)
                
                st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                grid = '<div class="grid-container">'
                for n in snips: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div></div>'
                st.markdown(grid, unsafe_allow_html=True)
            
            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            top5 = [x[0] for x in Counter(all_gen).most_common(5)]
            st.markdown(f"### ⚡ TOP 5 AUTO-PICK: {' | '.join([f'🎯 {x}' for x in top5])}")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.subheader("🔄 BBFS Ultra")
        # Logika BBFS tetap ada sesuai V7
        b_in = st.text_input("Input BBFS:")
        if st.button("PANGKAS 2D"):
            p = list(b_in)
            res_b = []
            for _ in range(15):
                random.shuffle(p)
                res_b.append("".join(p[:2]))
            st.write(list(set(res_b)))

else: st.error("Koneksi Database Gagal!")
