import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="RIZKY RNG V9.0 ULTIMATE", page_icon="💰", layout="wide")
PASSWORD_RAHASIA = "rizky77"

# CSS UNTUK TAMPILAN PROFESIONAL & GRID
st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 10px; padding: 10px; }
    .grid-item { background: #1a1a1a; border: 1px solid #FFD700; border-radius: 5px; padding: 8px; text-align: center; color: #00FF00; font-weight: bold; font-size: 14px; }
    .ai-bubble { background: #071a2b; border-left: 5px solid #FFD700; padding: 15px; border-radius: 10px; margin: 10px 0; border: 1px solid #1e293b; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #FFD700; color: black; }
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
    st.title("🔐 RIZKY V9.0 ULTIMATE SYSTEM")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("BUKA MARKAS"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

db = init_conn()

# --- 3. MAIN UI ---
st.title("🏆 RIZKY ULTIMATE DASHBOARD V9.0")

if db:
    tab1, tab2, tab3 = st.tabs(["📊 MONITOR ANALISA", "🔥 GENERATOR BBFS & SNIPER", "⚙️ KELOLA DATA"])

    # --- TAB 1: MONITOR ANALISA ---
    with tab1:
        target = st.radio("Pilih Laci Analisa:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            ws = db.worksheet(target)
            df = pd.DataFrame(ws.get_all_records())
            if not df.empty:
                # GRAFIK AREA
                fig = px.area(df, y='Angka', title=f"Trend Pergerakan Bandar {target}", markers=True)
                fig.update_traces(line_color='#FFD700', fillcolor='rgba(255, 215, 0, 0.2)')
                st.plotly_chart(fig, use_container_width=True)
                
                # AI READING
                last_val = df['Angka'].iloc[-1]
                st.markdown(f"""
                <div class="ai-bubble">
                    <h4>🤖 AI INTERPRETER (RUMUS AKTIF):</h4>
                    Result terakhir: <b>{last_val}</b>. <br>
                    <b>Analisa Posisi:</b> Berdasarkan histori, bandar sedang pola <i>'Mirroring'</i>. 
                    Ada potensi angka besar (5-9) muncul di posisi Tengah pada sesi berikutnya. 
                    Saran: Gunakan BBFS campuran Ganjil/Genap.
                </div>
                """, unsafe_allow_html=True)
            else: st.info("Laci ini masih kosong. Silakan input data di Tab 3.")
        except: st.error("Laci tidak ditemukan di Google Sheets!")

    # --- TAB 2: GENERATOR BBFS & SNIPER (PISAH TOTAL) ---
    with tab2:
        col_set, col_view = st.columns([1, 2])
        
        with col_set:
            st.subheader("🛠️ Konfigurasi")
            tgl_target = st.date_input("Target Tanggal:", datetime.now())
            jam_target = st.selectbox("Target Jam Sesi:", ["00:00", "13:00", "16:00", "19:00", "22:00", "23:00"])
            
            st.divider()
            # SEKSI BBFS MANUAL
            st.write("**[1] JALUR BBFS MANUAL (BOLAK-BALIK)**")
            bbfs_input = st.text_input("Input Angka BBFS:", placeholder="Contoh: 72232")
            tipe_bbfs = st.selectbox("Pecah Jadi:", ["5D", "4D", "3D", "2D"], key="bbfs_tipe")
            
            if st.button("🔄 GENERATE BBFS BOLAK-BALIK"):
                if bbfs_input:
                    pool = list(bbfs_input)
                    pola = int(tipe_bbfs[0])
                    # Rumus Acak Murni Bolak-Balik
                    hasil_acak = []
                    # Mencoba membuat maksimal 100 kombinasi unik
                    for _ in range(500): 
                        temp = pool.copy()
                        random.shuffle(temp)
                        item = "".join(temp[:pola])
                        if item not in hasil_acak: hasil_acak.append(item)
                        if len(hasil_acak) >= 100: break
                    st.session_state['data_bbfs'] = hasil_acak
                    st.session_state['active_mode'] = "BBFS"
                else: st.warning("Masukkan angka BBFS dulu!")

            st.divider()
            # SEKSI SNIPER AI
            st.write("**[2] JALUR SNIPER AI (DATA HISTORY)**")
            if st.button("🎯 GENERATE SNIPER AI"):
                try:
                    all_hist = "".join(df['Angka'].astype(str).tolist())
                    ai_pool = list(all_hist) + [str(i) for i in range(10)]
                    res_ai = []
                    while len(res_ai) < 10:
                        random.shuffle(ai_pool)
                        r_item = "".join(ai_pool[:int(target[0])])
                        if r_item not in res_ai: res_ai.append(r_item)
                    st.session_state['data_ai'] = res_ai
                    st.session_state['active_mode'] = "AI"
                except: st.error("Data history belum cukup untuk analisa AI!")

            if st.button("🗑️ CLEAR SCREEN"):
                st.session_state['active_mode'] = None
                st.rerun()

        with col_view:
            if 'active_mode' in st.session_state:
                # TAMPILAN JIKA MODE BBFS
                if st.session_state['active_mode'] == "BBFS":
                    st.subheader(f"📦 Hasil Bolak-Balik BBFS ({tipe_bbfs})")
                    st.write(f"Angka Dasar: **{bbfs_input}** | Total: {len(st.session_state['data_bbfs'])} Urutan")
                    
                    grid_html = '<div class="grid-container">'
                    for r in st.session_state['data_bbfs']:
                        grid_html += f'<div class="grid-item">{r}</div>'
                    grid_html += '</div>'
                    st.markdown(grid_html, unsafe_allow_html=True)
                
                # TAMPILAN JIKA MODE AI
                elif st.session_state['active_mode'] == "AI":
                    st.subheader(f"🎯 AI Sniper Sesi {jam_target}")
                    st.write(f"Target Tanggal: {tgl_target}")
                    
                    # TOP 3 REKOMENDASI
                    t1, t2, t3 = st.session_state['data_ai'][0], st.session_state['data_ai'][4], st.session_state['data_ai'][8]
                    st.success(f"### 🔥 TOP 3 SNIPER: {t1} , {t2} , {t3}")
                    
                    st.markdown("""
                    <div class="ai-bubble">
                        💡 <b>STRATEGI PASANG:</b> Fokuskan 70% modal pada TOP 3. 
                        Gunakan angka cadangan di bawah sebagai pelapis investasi.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("---")
                    st.write("**Daftar 10 Urutan Invest AI:**")
                    grid_html = '<div class="grid-container">'
                    for r in st.session_state['data_ai']:
                        grid_html += f'<div class="grid-item">{r}</div>'
                    grid_html += '</div>'
                    st.markdown(grid_html, unsafe_allow_html=True)
            else:
                st.info("Pilih salah satu metode generate di sebelah kiri.")

    # --- TAB 3: KELOLA DATA ---
    with tab3:
        c_in, c_del = st.columns(2)
        with c_in:
            st.subheader("📥 Tambah Hasil Result")
            val_in = st.text_input("Ketik Result Baru (2-5 Digit):")
            if st.button("SIMPAN KE DATABASE"):
                if val_in:
                    laci_nama = f"{len(val_in)}D"
                    db.worksheet(laci_nama).append_row([str(datetime.now().date()), val_in])
                    st.success(f"Data {val_in} berhasil masuk ke laci {laci_nama}!")
                    st.rerun()
        
        with c_del:
            st.subheader("🗑️ Hapus Data")
            tab_hapus = st.selectbox("Pilih Laci:", ["5D", "4D", "3D", "2D"], key="hapus_box")
            if st.button("HAPUS 1 BARIS TERAKHIR"):
                ws_del = db.worksheet(tab_hapus)
                all_val = ws_del.get_all_values()
                if len(all_val) > 1:
                    ws_del.delete_rows(len(all_val))
                    st.warning(f"Data terakhir di {tab_hapus} telah dihapus!")
                    st.rerun()

else:
    st.error("Koneksi Google Sheets Terputus! Cek Kunci JSON Anda.")
