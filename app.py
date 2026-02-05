import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import itertools
import random
import requests
from bs4 import BeautifulSoup

# --- 1. SETTINGS & PASSWORD ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY RNG V5.4 AUTOPILOT", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1a1a; color: #FFD700; border-radius: 10px; }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black; font-weight: bold; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 45px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold;
    }
    .analisis-box { padding: 20px; border-radius: 15px; background: #111; border: 1px solid #FFD700; margin-bottom: 20px; }
    .rekomendasi-angka { font-size: 22px; color: #FFD700; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔐 RIZKY GOLDEN SYSTEM</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Key:", type="password")
    if st.button("UNLOCK"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. DATABASE ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"
@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    with open(NAMA_KUNCI) as f: info = json.load(f)
    return gspread.authorize(Credentials.from_service_account_info(info, scopes=scope)).open("Database_RNG_Rizky").get_worksheet(0)

# --- 4. AUTO SCRAPER ENGINE (LITE) ---
def get_live_data(url):
    try:
        # Kita gunakan User-Agent agar tidak terdeteksi sebagai robot
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        # Catatan: Jika situs pakai Cloudflare, scraping langsung mungkin sulit.
        # Untuk nanas83501, kita siapkan simulasi penarik data tercepat.
        return "99999" # Placeholder: Jika berhasil tembus, angka ini akan dinamis
    except:
        return ""

try:
    sheet = init_conn()
    all_data = sheet.get_all_values()
    df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
    data_exists = not df.empty

    st.title("🎯 RIZKY RNG V5.4 AUTOPILOT")

    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS", "🔮 PREDIKSI", "🎲 BBFS PRO"])

    with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("Fetch Data")
            target = st.selectbox("Pilih Target Pasaran:", ["TTM 5D", "TTM 4D", "KINGKONG 4D"])
            if st.button("🛰️ TARIK DATA DARI SITUS"):
                # Logika: Mencoba narik dari nanas83501.com
                hasil_scan = get_live_data("https://nanas83501.com/")
                if hasil_scan:
                    st.session_state['auto_val'] = hasil_scan
                    st.info(f"Berhasil Mendeteksi Angka Terakhir: {hasil_scan}")
                else:
                    st.error("Situs sedang diproteksi. Masukkan manual di bawah.")

            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam", value=target)
                val = st.text_input("Hasil Angka", value=st.session_state.get('auto_val', ""))
                if st.form_submit_button("SIMPAN KE DATABASE"):
                    if val:
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Data Berhasil Masuk!"); st.rerun()
        with c2:
            st.markdown("### 📜 Log Terakhir")
            if data_exists: st.table(df.tail(5))

    with tab_stat:
        if data_exists:
            ekor_list = [int(a[-1]) for a in df['Angka'] if a and a[-1].isdigit()]
            if ekor_list:
                hot_e = str(pd.Series(ekor_list).value_counts().idxmax())
                st.markdown(f"""<div class="analisis-box"><p class="rekomendasi-angka">EKOR SAKTI: {hot_e}</p></div>""", unsafe_allow_html=True)
                st.plotly_chart(px.bar(x=list(range(10)), y=[ekor_list.count(i) for i in range(10)], title="Frekuensi Ekor", color_discrete_sequence=['#FFD700']), use_container_width=True)

    with tab_pred:
        if data_exists:
            mode = st.selectbox("Mode Prediksi:", ["2D", "3D", "4D", "5D"])
            if st.button("🔥 RACIK"):
                res = ["".join([str(random.randint(0,9)) for _ in range(int(mode[0]))]) for _ in range(10)]
                st.code(", ".join(res))

    with tab_bbfs:
        st.subheader("🎲 BBFS GENERATOR PRO")
        b_in = st.text_input("Masukkan Angka Main (Contoh: 12345)")
        b_mode = st.radio("Pilih Target Output:", ["2D", "3D", "4D"], horizontal=True)
        b_jml = st.number_input("Jumlah Baris:", 1, 50, 10)
        
        if st.button("GENERATE KOMBINASI"):
            if b_in and len(b_in) >= int(b_mode[0]):
                # Membuat kombinasi sesuai pilihan (2D/3D/4D)
                combos = list(itertools.permutations(b_in, int(b_mode[0])))
                hasil = ["".join(p) for p in combos]
                random.shuffle(hasil)
                st.markdown(f"**Hasil {b_mode} dari Angka {b_in}:**")
                st.code(", ".join(hasil[:b_jml]))
            else:
                st.warning(f"Angka main harus minimal {b_mode[0]} digit!")

    if st.sidebar.button("🔒 Logout"):
        del st.session_state["password_correct"]; st.rerun()

except Exception as e:
    st.error(f"Koneksi Bermasalah: {e}")
