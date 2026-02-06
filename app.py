import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="RIZKY V9.5 COMPLETE", page_icon="⚔️", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: 'Courier New'; font-size: 16px; font-weight: bold; }
    .ai-box { background: #001220; border-left: 10px solid #FF4B4B; padding: 20px; border-radius: 15px; color: white; border: 1px solid #333; }
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

if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V9.5 COMPLETE")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

db = init_conn()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 1. KELOLA DATA", "📊 2. ANALISIS AI", "🎯 3. SNIPER JITU", "🔄 4. BBFS ULTRA"])

    # --- TAB 1: KELOLA DATA ---
    with tab1:
        st.subheader("📥 Input Hasil Result")
        c1, c2 = st.columns(2)
        with c1: t_in = st.date_input("Tanggal:", datetime.now())
        with c2: a_in = st.text_input("Angka Result:", placeholder="Contoh: 8827")
        if st.button("💾 SIMPAN KE DATABASE"):
            if a_in:
                laci = f"{len(a_in)}D"
                db.worksheet(laci).append_row([str(t_in), a_in])
                st.success(f"Tersimpan di {laci}!"); st.rerun()

        st.divider()
        st.subheader("🗑️ History & Hapus")
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
                fig.update_traces(line_color='#FF4B4B')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f'<div class="ai-box">🤖 AI: Result {df_an["Angka"].iloc[-1]} terdeteksi. Gunakan tombol digit di Tab Sniper untuk eksekusi.</div>', unsafe_allow_html=True)
        except: st.warning("Data belum cukup.")

    # --- TAB 3: SNIPER JITU (FIXED 5D KEMBALI) ---
    with tab3:
        st.subheader("🎯 Sniper Target Digit")
        # Baris Tombol 5D dan 4D
        col_s1, col_s2 = st.columns(2)
        with col_s1: s5 = st.button("🔥 SNIPER 5D")
        with col_s2: s4 = st.button("🔥 SNIPER 4D")
        # Baris Tombol 3D dan 2D
        col_s3, col_s4 = st.columns(2)
        with col_s3: s3 = st.button("🔥 SNIPER 3D")
        with col_s4: s2 = st.button("🔥 SNIPER 2D")
        
        t_digit = None
        if s5: t_digit = 5
        if s4: t_digit = 4
        if s3: t_digit = 3
        if s2: t_digit = 2

        if t_digit:
            try:
                hist = "".join(df_an['Angka'].astype(str).tolist())
                pool = list(hist) + [str(i) for i in range(10)]
                snip = []
                while len(snip) < 10:
                    random.shuffle(pool)
                    r = "".join(pool[:t_digit])
                    if r not in snip: snip.append(r)
                st.success(f"### ⚔️ HASIL SNIPER {t_digit}D")
                st.markdown(f"## 🏆 UTAMA: {snip[0]} — {snip[3]} — {snip[7]}")
                grid = '<div class="grid-container">'
                for n in snip: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div>'; st.markdown(grid, unsafe_allow_html=True)
            except: st.error("Input data dulu di Tab 1!")

    # --- TAB 4: BBFS ULTRA (FIXED 5D KEMBALI) ---
    with tab4:
        st.subheader("🔄 Ultra BBFS Bolak-Balik")
        b_in = st.text_input("Ketik Angka BBFS:", placeholder="Contoh: 82731")
        # Baris Tombol 5D dan 4D
        col_b1, col_b2 = st.columns(2)
        with col_b1: b5 = st.button("💥 ACAK 5D")
        with col_b2: b4 = st.button("💥 ACAK 4D")
        # Baris Tombol 3D dan 2D
        col_b3, col_b4 = st.columns(2)
        with col_b3: b3 = st.button("💥 ACAK 3D")
        with col_b4: b2 = st.button("💥 ACAK 2D")
        
        b_t = None
        if b5: b_t = 5
        if b4: b_t = 4
        if b3: b_t = 3
        if b2: b_t = 2

        if b_t and b_in:
            pool_b = list(b_in); hasil = []
            for _ in range(1000):
                temp = pool_b.copy(); random.shuffle(temp)
                res = "".join(temp[:b_t])
                if res not in hasil: hasil.append(res)
                if len(hasil) >= 100: break
            st.info(f"Target: {b_t}D | BBFS: {b_in} | Total: {len(hasil)} Urutan")
            grid_b = '<div class="grid-container">'
            for x in hasil: grid_b += f'<div class="grid-item">{x}</div>'
            grid_b += '</div>'; st.markdown(grid_b, unsafe_allow_html=True)
        elif b_t and not b_in: st.warning("Masukkan angka BBFS dulu!")

else: st.error("Koneksi Error!")
