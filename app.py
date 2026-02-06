import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. SETTINGS & THEME ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY RNG V8.1 ULTIMATE", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1a1a; color: #FFD700; border-radius: 10px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 50px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold; font-size: 16px;
    }
    .box-ai { padding: 20px; border-radius: 15px; background: #111; border: 2px solid #FFD700; margin-bottom: 20px; }
    .gold-text { color: #FFD700; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"
@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        return gspread.authorize(Credentials.from_service_account_info(info, scopes=scope)).open("Database_RNG_Rizky").get_worksheet(0)
    except: return None

sheet = init_conn()
if sheet:
    all_data = sheet.get_all_values()
    df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
else:
    df = pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])

# --- 3. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔐 UNLOCK RIZKY GOLDEN SYSTEM V8.1</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Key:", type="password")
    if st.button("OPEN"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

st.title("🏆 RIZKY RNG ULTIMATE V8.1 (DATA INTEGRITY)")

tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS AI", "🔮 PREDIKSI JITU", "🎲 BBFS PRO"])

# --- TAB 1: DATA CENTER (INTEGRITY VERSION) ---
with tab_db:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🛰️ Input Real Data")
        with st.form("input_form"):
            tgl = st.date_input("Tanggal", datetime.now())
            sesi = st.selectbox("Tipe Pasaran", ["5D", "4D", "3D"])
            val = st.text_input("Angka Result")
            if st.form_submit_button("SIMPAN"):
                # Validasi Data Integrity: Cek apakah jumlah digit sesuai tipe
                if len(val) == int(sesi[0]) and sheet:
                    sheet.append_row([str(tgl), sesi, val])
                    st.success(f"Data {sesi} Berhasil Disimpan!")
                    st.rerun()
                else:
                    st.error(f"Salah! Untuk {sesi} wajib input {sesi[0]} digit.")
        
        st.markdown("---")
        st.subheader("🗑️ Danger Zone")
        confirm_del = st.checkbox("Saya sadar ingin menghapus semua data")
        if st.button("HAPUS SEMUA DATABASE"):
            if confirm_del and sheet:
                sheet.resize(rows=1); sheet.resize(rows=100)
                st.error("DATABASE DIBERSIHKAN!"); st.rerun()
    with c2:
        st.markdown("### 📜 History Data")
        st.table(df.tail(8))

# --- TAB 2: ANALISIS AI (HOT/COLD FILTERED) ---
with tab_stat:
    if not df.empty:
        # Filter data sesuai target untuk analisis lebih tajam
        target_ana = st.radio("Analisis Spesifik:", ["5D", "4D", "3D"], horizontal=True)
        df_filtered = df[df['Angka'].str.len() == int(target_ana[0])]
        
        if not df_filtered.empty:
            all_digits = "".join(df_filtered['Angka'].tolist())
            counts = pd.Series(list(all_digits)).value_counts()
            hot = counts.head(4).index.tolist()
            cold = counts.tail(3).index.tolist()
            
            st.markdown(f"""
            <div class="box-ai">
                <h3 class="gold-text">🤖 ANALISIS AI RIZKY (KHUSUS {target_ana})</h3>
                <p>Berdasarkan tren <b>RNG {target_ana}</b>, berikut saran angka:</p>
                <ul>
                    <li><b>Angka Kuat (Hot):</b> <span class="gold-text">{', '.join(hot)}</span></li>
                    <li><b>Angka Lemah (Cold):</b> <span class="gold-text">{', '.join(cold)}</span></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(px.bar(x=counts.index, y=counts.values, title=f"Distribusi Digit {target_ana}", color_discrete_sequence=['#FFD700']), use_container_width=True)
        else:
            st.info(f"Belum ada data khusus {target_ana} untuk dianalisis.")

# --- TAB 3: PREDIKSI (INTEGRITY ENGINE) ---
with tab_pred:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        mode_p = st.selectbox("Target Prediksi:", ["5D", "4D", "3D", "2D"])
        jml_urutan = st.number_input("Jumlah Urutan Hasil:", min_value=1, max_value=20, value=7)
    
    if st.button("🔥 GENERATE PREDIKSI KOMPLEKS"):
        # Filter data history sesuai target prediksi agar akurat
        digit_target = int(mode_p[0])
        df_logic = df[df['Angka'].str.len() == digit_target]
        
        if df_logic.empty:
            st.warning(f"Data {mode_p} sedikit, menggunakan database umum...")
            df_logic = df

        if not df_logic.empty:
            # Algoritma Kompleks: Data Berbobot + Last Result Multiplier
            last_res = df_logic['Angka'].iloc[-1]
            pool = list("".join(df_logic['Angka'].tolist())) + list(last_res)*3 + ([str(i) for i in range(10)] * 2)
            
            for i in range(jml_urutan):
                random.shuffle(pool)
                hasil = "".join(pool[:digit_target])
                st.markdown(f"**Urutan {i+1}:** `{hasil}`")
        else:
            st.error("Database benar-benar kosong!")

# --- TAB 4: BBFS 5D ---
with tab_bbfs:
    st.subheader("🎲 Jaring Pengaman BBFS PRO")
    angka_main = st.text_input("Masukkan 5-7 Angka Main:", value="02789")
    target_b = st.radio("Format Output:", ["4D", "3D", "2D"], horizontal=True)
    
    if st.button("GENERATE BBFS & BOLAK BALIK"):
        if len(angka_main) >= int(target_b[0]):
            combos = list(itertools.permutations(angka_main, int(target_b[0])))
            hasil_bb = ["".join(p) for p in combos]
            random.shuffle(hasil_bb)
            st.success(f"Berhasil meracik {len(hasil_bb)} pola Bolak-Balik!")
            st.markdown(f"**BBFS Utama Anda:** `{angka_main[:5]}`")
            st.write("---")
            st.write("Hasil Top 30 (Siap Pasang):")
            st.code(", ".join(hasil_bb[:30]))

if st.sidebar.button("🔒 Logout"):
    del st.session_state["password_correct"]; st.rerun()
