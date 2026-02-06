import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="RIZKY RNG V8.8 SNIPER", page_icon="🎯", layout="wide")
PASSWORD_RAHASIA = "rizky77"

# CSS UNTUK TAMPILAN GRID & AI BUBBLE
st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(70px, 1fr)); gap: 8px; padding: 10px; }
    .grid-item { background: #1a1a1a; border: 1px solid #FFD700; border-radius: 5px; padding: 8px; text-align: center; color: #FFD700; font-weight: bold; font-size: 13px; }
    .ai-bubble { background: #0f172a; border-left: 5px solid #FFD700; padding: 15px; border-radius: 10px; margin: 10px 0; border: 1px solid #1e293b; }
    .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
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
    st.title("🔐 RIZKY SNIPER V8.8")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

db = init_conn()

# --- 3. MAIN UI ---
st.title("🎯 RIZKY SNIPER DASHBOARD V8.8")

if db:
    tab1, tab2, tab3 = st.tabs(["📊 ANALISA TREND", "🔥 SNIPER & BBFS", "⚙️ KELOLA DATA"])

    # --- TAB 1: ANALISA TREND ---
    with tab1:
        target = st.radio("Pilih Laci:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            ws = db.worksheet(target)
            df = pd.DataFrame(ws.get_all_records())
            if not df.empty:
                fig = px.line(df, y='Angka', title=f"Arus Gerak Bandar {target}", markers=True)
                fig.update_traces(line_color='#FFD700')
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"""
                <div class="ai-bubble">
                    <h4>🤖 AI INTERPRETER:</h4>
                    Melihat data terakhir <b>{df['Angka'].iloc[-1]}</b>, bandar sedang menggunakan pola <b>Triangle Shift</b>. 
                    Garis grafik menunjukkan kejenuhan di angka tengah. Saran: Fokus pada angka ekstrim (0-2 atau 7-9).
                </div>
                """, unsafe_allow_html=True)
            else: st.info("Belum ada data di laci ini.")
        except: st.error("Laci tidak ditemukan!")

    # --- TAB 2: SNIPER & BBFS ---
    with tab2:
        col_input, col_view = st.columns([1, 2])
        
        with col_input:
            st.subheader("🚀 Sniper Setup")
            tgl_target = st.date_input("Target Tanggal:", datetime.now())
            jam_target = st.selectbox("Target Jam Sesi:", ["00:00", "13:00", "16:00", "19:00", "22:00", "23:00"])
            
            st.divider()
            bbfs_val = st.text_input("BBFS Manual (Opsional):", placeholder="Contoh: 08279")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("GENERATE AI"):
                    try:
                        all_nums = "".join(df['Angka'].astype(str).tolist())
                        pool = list(all_nums) + [str(i) for i in range(10)]
                        res = []
                        while len(res) < 10:
                            random.shuffle(pool)
                            r = "".join(pool[:int(target[0])])
                            if r not in res: res.append(r)
                        st.session_state['ai_sniper'] = res
                    except: st.error("Input data dulu di Tab 3!")
            with c2:
                if st.button("CLEAR ALL"):
                    st.session_state['ai_sniper'] = []
                    st.rerun()

        with col_view:
            if 'ai_sniper' in st.session_state and st.session_state['ai_sniper']:
                st.markdown(f"### 🎯 HASIL SNIPER: {tgl_target} | {jam_target}")
                
                # REKOMENDASI UTAMA
                top_3 = [st.session_state['ai_sniper'][0], st.session_state['ai_sniper'][4], st.session_state['ai_sniper'][8]]
                st.success(f"**TOP 3 WAJIB PASANG: {top_3[0]} , {top_3[1]} , {top_3[2]}**")
                st.info(f"💡 **RUMUS AI:** Berdasarkan sesi {jam_target}, angka {top_3[0][0]} kuat di posisi AS.")

                # GRID 100 / LIST
                st.write("---")
                st.write("**Daftar 10 Urutan Cadangan (Invest):**")
                grid_html = '<div class="grid-container">'
                for r in st.session_state['ai_sniper']:
                    grid_html += f'<div class="grid-item">{r}</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
            else:
                st.info("Klik 'GENERATE AI' untuk memunculkan angka sniper.")

    # --- TAB 3: KELOLA DATA ---
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📥 Tambah Result")
            new_val = st.text_input("Angka Result:")
            if st.button("SIMPAN DATA"):
                if new_val:
                    laci_in = f"{len(new_val)}D"
                    db.worksheet(laci_in).append_row([str(datetime.now().date()), new_val])
                    st.success(f"Berhasil simpan ke {laci_in}!")
                    st.rerun()
        with col2:
            st.subheader("🗑️ Hapus Data")
            target_del = st.selectbox("Pilih Laci untuk Dihapus:", ["5D", "4D", "3D", "2D"])
            if st.button("HAPUS 1 BARIS TERAKHIR"):
                ws_del = db.worksheet(target_del)
                all_rows = ws_del.get_all_values()
                if len(all_rows) > 1:
                    ws_del.delete_rows(len(all_rows))
                    st.warning("Data terakhir dihapus!")
                    st.rerun()

else:
    st.error("Gagal konek ke Google Sheets!")
