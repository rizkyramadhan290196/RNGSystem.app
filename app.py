import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. SETTINGS & FULL SECURITY ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY RNG V7.0 ULTIMATE GOLD", page_icon="🚀", layout="wide")

# CSS MEWAH (KEMBALI KE GOLD THEME)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1a1a; color: #FFD700; border-radius: 10px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 50px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold; font-size: 18px; border: none;
    }
    .box-jp { padding: 25px; border-radius: 15px; background: #111; border: 2px solid #FFD700; text-align: center; margin-bottom: 20px; }
    .angka-bbfs { font-size: 40px; color: #FFD700; font-weight: bold; letter-spacing: 8px; }
    </style>
    """, unsafe_allow_html=True)

if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔐 RIZKY GOLDEN SYSTEM V7.0</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Key:", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 2. DATABASE CONNECTION (KEMBALI OTOMATIS) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"
@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        return gspread.authorize(Credentials.from_service_account_info(info, scopes=scope)).open("Database_RNG_Rizky").get_worksheet(0)
    except Exception as e:
        st.error(f"Koneksi Database Gagal: {e}")
        return None

sheet = init_conn()
if sheet:
    all_data = sheet.get_all_values()
    df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
    df['Angka'] = df['Angka'].astype(str).str.strip()
else:
    df = pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])

data_exists = not df.empty

# --- 3. CORE LOGICA RNG BANDAR (KOMPLEKS) ---
def logic_rng_v7(df_input, target_digit, jumlah_baris):
    if df_input.empty: return [], []
    
    # Ambil database mentah
    raw_digits = "".join(df_input['Angka'].tolist())
    counts = pd.Series(list(raw_digits)).value_counts()
    
    # 1. Analisis Hot (Sering Keluar)
    hot_nums = counts.head(6).index.tolist()
    # 2. Analisis Cold (Jarang Keluar / Simpanan Bandar)
    cold_nums = counts.tail(4).index.tolist()
    # 3. Analisis Posisi Akhir (Ekor)
    ekor_list = [a[-1] for a in df_input['Angka'] if a]
    hot_ekor = pd.Series(ekor_list).value_counts().idxmax()

    # PEMBUATAN POOL BERBOBOT (95% Simulasi Bandar)
    # Bandar = 60% Hot + 25% Cold + 15% Shuffle
    pool = (hot_nums * 10) + (cold_nums * 5) + [str(i) for i in range(10)]
    
    results = []
    for _ in range(jumlah_baris):
        random.shuffle(pool)
        # Ambil angka dengan menjaga probabilitas ekor sakti
        res = "".join(pool[:target_digit-1]) + str(hot_ekor if random.random() > 0.5 else random.choice(pool))
        results.append(res[:target_digit])
    
    # BBFS 5D (Kombinasi Terbaik)
    bbfs_raw = sorted(list(set(hot_nums[:3] + cold_nums[:2])))
    return results, bbfs_raw[:5]

# --- 4. MAIN UI ---
st.title("🎯 RIZKY RNG ULTIMATE V7.0 GOLD")

tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 STATISTIK", "🔮 PREDIKSI", "🎲 BBFS PRO"])

with tab_db:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🛰️ Input Real Data")
        with st.form("input_form"):
            tgl = st.date_input("Tanggal", datetime.now())
            jam = st.selectbox("Sesi", ["TTM 5D", "TTM 4D", "KINGKONG 4D"])
            val = st.text_input("Hasil Angka (Wajib 5 Digit)")
            if st.form_submit_button("SIMPAN KE GOOGLE SHEETS"):
                if len(val) >= 4 and sheet:
                    sheet.append_row([str(tgl), jam, val])
                    st.success("Data Berhasil Sinkron!"); st.rerun()
    with c2:
        st.markdown("### 📜 Log Data Terakhir")
        st.dataframe(df.tail(10), use_container_width=True)
        if st.button("🗑️ Hapus Baris Terakhir"):
            if sheet: sheet.delete_rows(len(all_data)); st.rerun()

with tab_stat:
    if data_exists:
        st.subheader("📊 Analisis Frekuensi RNG")
        all_digits = "".join(df['Angka'].tolist())
        digit_counts = pd.Series(list(all_digits)).value_counts().sort_index()
        fig = px.bar(x=digit_counts.index, y=digit_counts.values, title="Distribusi Angka Bandar", color_discrete_sequence=['#FFD700'])
        st.plotly_chart(fig, use_container_width=True)

with tab_pred:
    st.subheader("🔮 Generator V7.0 (Mendekati RNG Bandar)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        mode_p = st.selectbox("Mode Target:", ["5D", "4D", "3D", "2D"])
        jml_p = st.slider("Jumlah Baris:", 1, 20, 10)
    
    if st.button("🚀 GENERATE ANGKA JITU"):
        if data_exists:
            hasil, bbfs_saran = logic_rng_v7(df, int(mode_p[0]), jml_p)
            
            st.markdown('<div class="box-jp">', unsafe_allow_html=True)
            st.write("💰 **SARAN BBFS 5D (PENGAMAN):**")
            st.markdown(f'<div class="angka-bbfs">{" ".join(bbfs_saran)}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### 🎯 Urutan Tembakan:")
            cols = st.columns(2)
            for i, h in enumerate(hasil):
                cols[i%2].code(f"URUTAN {i+1}: {h}")
        else:
            st.error("Isi database dulu!")

with tab_bbfs:
    st.subheader("🎲 Pola Tarung & BBFS Generator")
    b_in = st.text_input("Masukkan Angka Main (Contoh: 02789)")
    b_mode = st.radio("Target:", ["4D", "3D", "2D"], horizontal=True)
    if st.button("GENERATE BBFS FULL"):
        if len(b_in) >= int(b_mode[0]):
            combos = list(itertools.permutations(b_in, int(b_mode[0])))
            hasil_b = ["".join(p) for p in combos]
            random.shuffle(hasil_b)
            st.write(f"Berhasil Generate {len(hasil_b)} kombinasi. Menampilkan 30 acak:")
            st.code(", ".join(hasil_b[:30]))

if st.sidebar.button("🔒 Logout"):
    del st.session_state["password_correct"]; st.rerun()
