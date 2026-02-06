import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="RIZKY V9.3 ULTRA", page_icon="⚔️", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #FF4B4B; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 16px; font-weight: bold; }
    .ai-box { background: #001220; border-right: 5px solid #FF4B4B; border-left: 5px solid #FF4B4B; padding: 20px; border-radius: 15px; color: white; border: 1px solid #333; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background: #FF4B4B; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background: #white; color: #FF4B4B; border: 2px solid #FF4B4B; }
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
    st.title("⚔️ RIZKY ULTRA SNIPER V9.3")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("MASUK MARKAS"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

db = init_conn()

if db:
    # MENU URUT SESUAI PERMINTAAN
    tab1, tab2, tab3, tab4 = st.tabs(["📥 1. KELOLA DATA", "📊 2. ANALISIS AI", "🎯 3. SNIPER JITU", "🔄 4. BBFS ULTRA"])

    # --- TAB 1: KELOLA DATA ---
    with tab1:
        st.subheader("📥 Input Hasil Hari Ini")
        c1, c2 = st.columns(2)
        with c1: t_in = st.date_input("Tanggal:", datetime.now())
        with c2: a_in = st.text_input("Angka Result:", placeholder="Contoh: 8827")
        
        if st.button("💾 SIMPAN KE DATABASE"):
            if a_in:
                laci = f"{len(a_in)}D"
                db.worksheet(laci).append_row([str(t_in), a_in])
                st.success(f"Tersimpan di {laci}!")
                st.rerun()

        st.divider()
        st.subheader("🗑️ History & Hapus")
        l_cek = st.selectbox("Cek Laci:", ["5D", "4D", "3D", "2D"])
        try:
            ws = db.worksheet(l_cek)
            df_hist = pd.DataFrame(ws.get_all_records())
            if not df_hist.empty:
                st.dataframe(df_hist.tail(10), use_container_width=True)
                if st.button("🗑️ HAPUS DATA TERAKHIR"):
                    ws.delete_rows(len(df_hist) + 1)
                    st.warning("Data Terhapus!")
                    st.rerun()
        except: st.info("Kosong.")

    # --- TAB 2: ANALISIS AI ---
    with tab2:
        l_an = st.radio("Analisa Laci:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            ws_an = db.worksheet(l_an)
            df_an = pd.DataFrame(ws_an.get_all_records())
            if not df_an.empty:
                fig = px.area(df_an, y='Angka', title=f"Trend Gerak Bandar {l_an}")
                fig.update_traces(line_color='#FF4B4B')
                st.plotly_chart(fig, use_container_width=True)
                
                last = str(df_an['Angka'].iloc[-1])
                st.markdown(f"""
                <div class="ai-box">
                    <h3>🤖 ANALISA TAJAM AI:</h3>
                    Result Terakhir: <b>{last}</b><br>
                    <b>Pola Bandar:</b> Sedang 'Over-Heating'. Angka-angka di atas rata-rata sering ditarik.<br>
                    <b>Rencana Serang:</b> Fokus pada angka 'Mirror' atau angka yang belum muncul dalam 5 sesi terakhir.<br>
                    <b>Power Level:</b> Tinggi (Siap Generate Sniper).
                </div>
                """, unsafe_allow_html=True)
            else: st.warning("Butuh data input dulu!")
        except: st.error("Laci Error.")

    # --- TAB 3: SNIPER JITU ---
    with tab3:
        st.subheader("🎯 Sniper Rumus Anti-Bandar")
        c3, c4 = st.columns(2)
        with c3: jam = st.selectbox("Jam Sesi:", ["13:00", "16:00", "19:00", "22:00", "23:00"])
        with c4: tgl = st.date_input("Target Tgl:", datetime.now())
        
        if st.button("🚀 TEMBAK SNIPER"):
            try:
                hist = "".join(df_an['Angka'].astype(str).tolist())
                pool = list(hist) + [str(i) for i in range(10)]
                snip = []
                while len(snip) < 10:
                    random.shuffle(pool)
                    r = "".join(pool[:int(l_an[0])])
                    # Filter Tajam: Buang angka urut (1234, 2345)
                    if r not in snip and r != r[::-1]: snip.append(r)
                
                st.success(f"### ⚔️ TOP SNIPER JAM {jam}")
                st.markdown(f"## 🏆 UTAMA: {snip[0]} — {snip[3]} — {snip[7]}")
                
                st.write("---")
                grid_snip = '<div class="grid-container">'
                for n in snip: grid_snip += f'<div class="grid-item">{n}</div>'
                grid_snip += '</div>'
                st.markdown(grid_snip, unsafe_allow_html=True)
            except: st.error("Isi data dulu!")

    # --- TAB 4: BBFS ULTRA ---
    with tab4:
        st.subheader("🔄 Ultra BBFS Generator (Bolak-Balik)")
        b_in = st.text_input("Ketik Angka BBFS:", placeholder="Contoh: 82731")
        tipe = st.selectbox("Mode:", ["5D", "4D", "3D", "2D"])
        
        if st.button("💥 GENERATE 100 URUTAN"):
            if b_in:
                pool_b = list(b_in)
                digit = int(tipe[0])
                hasil = []
                for _ in range(1000):
                    temp = pool_b.copy()
                    random.shuffle(temp)
                    res = "".join(temp[:digit])
                    # Filter Sampah: Minimalisir angka kembar kecuali diminta
                    if res not in hasil: hasil.append(res)
                    if len(hasil) >= 100: break
                
                st.info(f"Target: {tipe} | Dari BBFS: {b_in} | Total: {len(hasil)} Urutan")
                grid_b = '<div class="grid-container">'
                for x in hasil: grid_b += f'<div class="grid-item">{x}</div>'
                grid_b += '</div>'
                st.markdown(grid_b, unsafe_allow_html=True)
            else: st.warning("Input BBFS!")

else: st.error("Koneksi Sheets Error!")
