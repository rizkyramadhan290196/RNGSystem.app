import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="RIZKY V11.4 - RESONANSI ARUS", page_icon="📈", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 16px; font-weight: bold; }
    .slot-box { background: #001220; border: 2px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 15px; position: relative; }
    .slot-title { color: #FFD700; font-weight: bold; border-bottom: 1px solid #444; margin-bottom: 8px; font-size: 14px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; height: 3.5em; background-color: #1a1a1a; color: white; }
    .autopick-box { background: linear-gradient(45deg, #001f3f, #000000); border: 2px solid #00FF00; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-top: 20px; box-shadow: 0px 0px 15px #00FF00; }
    .mode-invest { background:#001220; border:2px solid #00FF00; padding:15px; border-radius:10px; text-align:center; margin-bottom:10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC CORE (V11.4 - RESONANSI HUNTER) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except: return None

def hitung_triangle_v11(res_str):
    """Rumus Triangle V11: Deteksi Sudut & Resonansi"""
    try:
        n = [int(d) for d in str(res_str) if d.isdigit()]
        if len(n) >= 5:
            # Menggunakan offset baru untuk menangkap angka tengah
            v1 = (n[0] + n[2] + 4) % 10 
            v2 = (n[1] + n[3] + 6) % 10 
            v3 = (n[-1] * 2 + 3) % 10 
            return f"{v1}{v2}{v3}{v1}"
        return "7634"
    except: return "7634"

def generate_pool_hunter(invest_str, bom_str, history_str):
    """
    Sistem Resonansi:
    Mengambil history lebih panjang (-40) agar angka sisa tetap terbaca.
    """
    short_hist = history_str[-40:] if history_str else ""
    # Bobot diseimbangkan (4:6:3)
    pool = list(invest_str) * 4 + list(bom_str) * 6 + list(short_hist) * 3
    
    # Mistik & Indeks Map
    m_map = {'0':'7','1':'0','7':'0','4':'9','9':'4','5':'8','8':'5','2':'5','3':'8','6':'9'}
    for char in (invest_str + bom_str):
        if char in m_map: pool.append(m_map[char])
        
    # Jumper RNG untuk antisipasi lompatan liar
    pool.extend([str(random.randint(0, 9)) for _ in range(5)])
    return [c for c in pool if c.isdigit()]

db = init_conn()

# --- 3. UI APP ---
if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V11.4 - RESONANSI ARUS")
    pwd = st.text_input("Kunci Akses:", type="password")
    if st.button("UNLOCK"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATA", "📊 ANALISIS", "🎯 SNIPER AI", "🔄 BBFS"])
    ws = db.worksheet("5D")
    df = pd.DataFrame(ws.get_all_records())

    with tab1:
        st.subheader("📥 Input Result 5D")
        a_in = st.text_input("Input Angka (Contoh: 76341):")
        if st.button("💾 SIMPAN DATA"):
            if a_in:
                ws.append_row([str(datetime.now().date()), a_in])
                st.success(f"Data {a_in} Tersimpan!")
                st.rerun()

    with tab2:
        st.subheader("📊 Grafik Tren Arus (Radar)")
        if not df.empty:
            # Ambil 2D belakang untuk radar grafik
            df['Ekor2D'] = df['Angka'].apply(lambda x: int(str(x)[-2:]) if len(str(x))>=2 else 0)
            st.line_chart(df['Ekor2D'].tail(30))
            st.info("Radar memantau pergerakan 30 result terakhir.")
        else:
            st.warning("Data kosong, silakan input di Tab 1.")

    with tab3:
        st.subheader("🎯 Sniper AI (Resonansi Mode)")
        cs1, cs2, cs3, cs4 = st.columns(4)
        with cs1: 
            if st.button("🔥 5D"): st.session_state['v_digit'] = 5
        with cs2: 
            if st.button("🔥 4D"): st.session_state['v_digit'] = 4
        with cs3: 
            if st.button("🔥 3D"): st.session_state['v_digit'] = 3
        with cs4: 
            if st.button("🔥 2D"): st.session_state['v_digit'] = 2
        
        t_digit = st.session_state.get('v_digit', 2)
        st.write(f"Mode Aktif: **{t_digit}D**")

        if not df.empty:
            res_akhir = str(df['Angka'].iloc[-1])
            hist_full = "".join(df['Angka'].astype(str).tolist())
            
            # Triangle & RNG Hunter
            bom_tri = hitung_triangle_v11(res_akhir)[:t_digit]
            r1 = "".join(random.sample(hist_full, t_digit)) if len(hist_full) >= t_digit else "76"
            r2 = "".join(random.sample(hist_full, t_digit)) if len(hist_full) >= t_digit else "41"
            
            st.markdown(f'<div class="mode-invest">🛡️ INVESTASI: {r1} — {r2} | 🔥 BOM TRI: {bom_tri}</div>', unsafe_allow_html=True)
            
            pool = generate_pool_hunter(r1+r2, bom_tri, hist_full)
            all_gen = []
            
            for i in range(1, 4):
                snips = []
                # Slot 3 tetap punya suara terkuat (Bobot 3x)
                weight_val = 3 if i == 3 else 1
                
                while len(snips) < 10:
                    random.shuffle(pool)
                    res = "".join(pool[:t_digit])
                    if res not in snips:
                        snips.append(res)
                        for _ in range(weight_val):
                            all_gen.append(res)
                
                st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i} {"(RESONANSI UTAMA)" if i==3 else ""}</div>', unsafe_allow_html=True)
                grid = '<div class="grid-container">'
                for n in snips: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div></div>'
                st.markdown(grid, unsafe_allow_html=True)
            
            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            top5 = [x[0] for x in Counter(all_gen).most_common(5)]
            st.markdown(f"### ⚡ TOP 5 AUTO-PICK: {' | '.join([f'🎯 {x}' for x in top5])}")
            st.markdown("<p style='font-size:12px;'>V11.4: Menyeimbangkan angka baru dan angka sisa (Resonansi).</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.subheader("🔄 BBFS Ultra Smart")
        b_in = st.text_input("Masukkan Angka BBFS:")
        if b_in and st.button("PANGKAS 2D"):
            p = [c for c in b_in if c.isdigit()]
            if len(p) >= 2:
                hasil = []
                for _ in range(5000):
                    random.shuffle(p)
                    res = "".join(p[:2])
                    if res not in hasil: hasil.append(res);
                    if len(hasil) >= 15: break
                st.write(f"15 Line Pangkasan: {', '.join(hasil)}")

else:
    st.error("Gagal menyambung ke Google Sheets. Cek file JSON kamu!")
