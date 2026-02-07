import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="RIZKY V9.7 AI ASSIST", page_icon="⚔️", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 5px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 4px; padding: 5px; text-align: center; color: #00FF00; font-family: monospace; font-size: 14px; font-weight: bold; }
    .slot-box { background: #001220; border: 1px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .slot-title { color: #FFD700; font-weight: bold; border-bottom: 1px solid #444; margin-bottom: 8px; font-size: 14px; }
    .ai-assist-box { background: linear-gradient(145deg, #071a2b, #000); border: 2px solid #00FF00; padding: 20px; border-radius: 15px; margin-bottom: 25px; text-align: center; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
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

if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V9.7 AI ASSIST")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 1. KELOLA DATA", "📊 2. ANALISIS AI", "🎯 3. PENTA-SNIPER AI", "🔄 4. BBFS ULTRA"])

    # --- TAB 1: KELOLA DATA ---
    with tab1:
        st.subheader("📥 Input Hasil Result")
        c1, c2 = st.columns(2)
        with c1: t_in = st.date_input("Tanggal:", datetime.now())
        with c2: a_in = st.text_input("Angka Result:", placeholder="Contoh: 8827")
        if st.button("💾 SIMPAN & KUNCI RUMUS"):
            if a_in:
                laci = f"{len(a_in)}D"
                db.worksheet(laci).append_row([str(t_in), a_in])
                st.success(f"Data Masuk! AI sedang mengkalibrasi ulang 5 Slot Sniper...")
                st.rerun()

        st.divider()
        l_cek = st.selectbox("Cek Laci:", ["5D", "4D", "3D", "2D"])
        try:
            ws = db.worksheet(l_cek)
            df_hist = pd.DataFrame(ws.get_all_records())
            if not df_hist.empty:
                st.dataframe(df_hist.tail(10), use_container_width=True)
                if st.button("🗑️ HAPUS DATA TERAKHIR"):
                    ws.delete_rows(len(df_hist) + 1); st.rerun()
        except: st.info("Kosong.")

    # --- TAB 2: ANALISIS AI ---
    with tab2:
        l_an = st.radio("Analisa Laci:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            ws_an = db.worksheet(l_an)
            df_an = pd.DataFrame(ws_an.get_all_records())
            if not df_an.empty:
                fig = px.area(df_an, y='Angka', title=f"Trend Gerak {l_an}")
                fig.update_traces(line_color='#00FF00')
                st.plotly_chart(fig, use_container_width=True)
        except: st.warning("Butuh data input dulu.")

    # --- TAB 3: PENTA-SNIPER + AI RECOMMENDATION ---
    with tab3:
        st.subheader("🎯 Sniper AI System")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1: s5 = st.button("🔥 SNIPER 5D")
        with col_s2: s4 = st.button("🔥 SNIPER 4D")
        with col_s3: s3 = st.button("🔥 SNIPER 3D")
        with col_s4: s2 = st.button("🔥 SNIPER 2D")

        t_digit = st.session_state.get('last_digit_v9', None)
        if s5: t_digit = 5
        if s4: t_digit = 4
        if s3: t_digit = 3
        if s2: t_digit = 2
        
        if t_digit:
            st.session_state['last_digit_v9'] = t_digit
            try:
                hist_str = "".join(df_an['Angka'].astype(str).tolist())
                # LOCKED SEED: Angka paten selama data tidak berubah
                random.seed(len(hist_str) * t_digit) 
                
                # --- ASISTEN AI REKOMENDASI UTAMA ---
                pool_ai = list(hist_str) + [str(j) for j in range(10)]
                random.shuffle(pool_ai)
                rec1 = "".join(pool_ai[:t_digit])
                random.shuffle(pool_ai)
                rec2 = "".join(pool_ai[:t_digit])
                random.shuffle(pool_ai)
                rec3 = "".join(pool_ai[:t_digit])

                st.markdown(f"""
                <div class="ai-assist-box">
                    <h3 style="color:#00FF00; margin-bottom:5px;">🤖 ASISTEN AI REKOMENDASI (100% RUMUS)</h3>
                    <p style="color:white;">Berdasarkan pola data {t_digit}D, pasang angka bom ini:</p>
                    <h1 style="color:#FFD700; letter-spacing: 5px;">{rec1} — {rec2} — {rec3}</h1>
                </div>
                """, unsafe_allow_html=True)

                # --- 5 SLOT INVESTASI (10 URUTAN PER SLOT) ---
                st.write(f"**📦 5 SLOT INVESTASI {t_digit}D (LOCKED):**")
                cols = st.columns(1) # Stacked for mobile readability
                
                for i in range(1, 6):
                    with st.container():
                        st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                        snip_list = []
                        while len(snip_list) < 10:
                            pool = list(hist_str) + [str(j) for j in range(10)]
                            random.shuffle(pool)
                            r = "".join(pool[:t_digit])
                            if r not in snip_list: snip_list.append(r)
                        
                        grid = '<div class="grid-container">'
                        for n in snip_list: grid += f'<div class="grid-item">{n}</div>'
                        grid += '</div></div>'
                        st.markdown(grid, unsafe_allow_html=True)
            except: st.error("Lengkapi data di Tab 1 dulu!")

    # --- TAB 4: BBFS ULTRA ---
    with tab4:
        st.subheader("🔄 BBFS Ultra Locked")
        b_in = st.text_input("Ketik Angka BBFS:", key="bbfs_input")
        c_b1, c_b2, c_b3, c_b4 = st.columns(4)
        with c_b1: b5 = st.button("💥 5D"); bt=5 if b5 else None
        with c_b2: b4 = st.button("💥 4D"); bt=4 if b4 else None
        with c_b3: b3 = st.button("💥 3D"); bt=3 if b3 else None
        with c_b4: b2 = st.button("💥 2D"); bt=2 if b2 else None
        
        if (b5 or b4 or b3 or b2) and b_in:
            random.seed(len(b_in) + 77) 
            hasil = []
            pool_b = list(b_in)
            for _ in range(500):
                temp = pool_b.copy(); random.shuffle(temp)
                res = "".join(temp[:bt])
                if res not in hasil: hasil.append(res)
                if len(hasil) >= 100: break
            
            grid_b = '<div class="grid-container">'
            for x in hasil: grid_b += f'<div class="grid-item">{x}</div>'
            grid_b += '</div>'; st.markdown(grid_b, unsafe_allow_html=True)

else: st.error("Database Diskonek!")
