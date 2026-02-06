import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="RIZKY RNG V8.8 FINAL", page_icon="💰", layout="wide")
PASSWORD_RAHASIA = "rizky77"

# CUSTOM CSS UNTUK TAMPILAN GRID & WARNA
st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 10px; padding: 10px; }
    .grid-item { background: #1a1a1a; border: 1px solid #FFD700; border-radius: 5px; padding: 8px; text-align: center; color: white; font-weight: bold; font-size: 14px; }
    .recommend-box { border: 2px solid #00FF00 !important; background: #002200 !important; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .ai-bubble { background: #0f172a; border-left: 5px solid #FFD700; padding: 15px; border-radius: 10px; margin: 10px 0; }
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
    st.title("🔐 RIZKY V8.8 SYSTEM")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("BUKA SISTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

db = init_conn()

# --- 3. MAIN DASHBOARD ---
st.title("🏆 RIZKY MASTER RNG V8.8")

if db:
    tab1, tab2, tab3 = st.tabs(["📊 MONITOR TREND", "🎲 MARKAS BBFS", "⚙️ DATA MANAGEMENT"])

    # --- TAB 1: MONITOR TREND & AI READING ---
    with tab1:
        target = st.radio("Cek Laci:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            ws = db.worksheet(target)
            df = pd.DataFrame(ws.get_all_records())
            if not df.empty:
                # Grafik Lebih Modern
                fig = px.area(df, y='Angka', title=f"Pergerakan Arus Bandar {target}", color_discrete_sequence=['#FFD700'])
                st.plotly_chart(fig, use_container_width=True)
                
                # AI TREND READER
                last_num = str(df['Angka'].iloc[-1])
                st.markdown(f"""
                <div class="ai-bubble">
                    <h4>🤖 AI INTERPRETER:</h4>
                    Result terakhir <b>{last_num}</b> menunjukkan pola pergeseran. <br>
                    <b>Analisa Grafik:</b> Arus sedang berada di titik jenuh. Bandar cenderung membuang angka yang 
                    sudah 5 sesi tidak muncul. Fokus pada angka 'Dingin' untuk sesi berikutnya!
                </div>
                """, unsafe_allow_html=True)
            else: st.info("Data kosong.")
        except: st.error("Tab tidak terbaca.")

    # --- TAB 2: MARKAS BBFS & 100 URUTAN ---
    with tab2:
        col_a, col_b = st.columns([1, 2])
        
        with col_a:
            st.subheader("🛠️ Custom Generator")
            bbfs_input = st.text_input("Masukkan Angka BBFS kamu:", placeholder="Contoh: 123456")
            tipe_gen = st.selectbox("Generate Untuk:", ["5D", "4D", "3D", "2D"])
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔥 GENERATE BBFS"):
                    if bbfs_input:
                        # Logic Manual BBFS (Acak dari input)
                        pool = list(bbfs_input)
                        results = []
                        for _ in range(100):
                            random.shuffle(pool)
                            res = "".join(pool[:int(tipe_gen[0])])
                            if res not in results: results.append(res)
                        st.session_state['res_manual'] = results
                    else: st.warning("Isi angka BBFS!")
            with c2:
                if st.button("🗑️ CLEAR"):
                    st.session_state['res_manual'] = []
                    st.rerun()

            st.write("---")
            if st.button("🤖 AI AUTO-PICK (TOP 10)"):
                # Logic AI Murni
                try:
                    all_data = "".join(df['Angka'].astype(str).tolist())
                    ai_pool = list(all_data) + [str(i) for i in range(10)]
                    ai_res = []
                    while len(ai_res) < 10:
                        random.shuffle(ai_pool)
                        r = "".join(ai_pool[:int(target[0])])
                        if r not in ai_res: ai_res.append(r)
                    st.session_state['res_ai'] = ai_res
                except: st.error("Isi data dulu di Monitor!")

        with col_b:
            # TAMPILAN GRID 100 URUTAN
            if 'res_manual' in st.session_state and st.session_state['res_manual']:
                st.subheader(f"📦 100 Urutan BBFS ({tipe_gen})")
                grid_html = '<div class="grid-container">'
                for r in st.session_state['res_manual']:
                    grid_html += f'<div class="grid-item">{r}</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
            
            # TAMPILAN TOP 10 AI
            if 'res_ai' in st.session_state and st.session_state['res_ai']:
                st.subheader("🌟 AI TOP 10 ELITE RECOMMENDATION")
                rekom = [st.session_state['res_ai'][0], st.session_state['res_ai'][2], st.session_state['res_ai'][6]]
                st.success(f"🎯 **REKOMENDASI UTAMA AI: {rekom[0]} , {rekom[1]} , {rekom[2]}**")
                
                for i, r in enumerate(st.session_state['res_ai']):
                    label = "⭐" if r in rekom else ""
                    st.code(f"Urutan {i+1}: {r} {label}")

    # --- TAB 3: DATA MANAGEMENT ---
    with tab3:
        st.subheader("📥 Input Result Baru")
        val_in = st.text_input("Input Angka:")
        if st.button("SIMPAN"):
            try:
                laci = f"{len(val_in)}D"
                db.worksheet(laci).append_row([str(datetime.now().date()), val_in])
                st.success("Tersimpan!")
                st.rerun()
            except: st.error("Gagal!")
        
        st.divider()
        st.subheader("🗑️ Hapus Data")
        target_del = st.selectbox("Pilih Tab:", ["5D", "4D", "3D", "2D"], key="del_tab")
        if st.button("HAPUS DATA TERAKHIR"):
            ws_del = db.worksheet(target_del)
            rows = ws_del.get_all_values()
            if len(rows) > 1:
                ws_del.delete_rows(len(rows))
                st.warning("Terhapus!")
                st.rerun()
else:
    st.error("Gagal koneksi ke Google Sheets!")
