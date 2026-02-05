import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. SETTINGS & PASSWORD ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY RNG V6.0 ULTIMATE", page_icon="🚀", layout="wide")

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
    .bbfs-box { padding: 15px; background: #1a1a1a; border-left: 5px solid #FFD700; border-radius: 8px; margin: 10px 0; }
    .highlight-gold { color: #FFD700; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔐 RIZKY GOLDEN SYSTEM V6.0</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Key:", type="password")
    if st.button("UNLOCK"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. DATABASE CONNECTION ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"
@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        return gspread.authorize(Credentials.from_service_account_info(info, scopes=scope)).open("Database_RNG_Rizky").get_worksheet(0)
    except:
        return None

try:
    sheet = init_conn()
    if sheet:
        all_data = sheet.get_all_values()
        df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
        df['Angka'] = df['Angka'].astype(str).str.strip()
    else:
        df = pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
    
    data_exists = not df.empty

    st.title("🎯 RIZKY RNG ULTIMATE V6.0")

    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS", "🔮 PREDIKSI ULTIMATE", "🎲 BBFS PRO V6"])

    # --- TAB 1: DATA CENTER ---
    with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("🛰️ Input Data")
            target = st.selectbox("Pilih Pasaran:", ["TTM 5D", "TTM 4D", "KINGKONG 4D"])
            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam", value=target)
                val = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if val.isdigit() and sheet:
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Tersimpan!"); st.rerun()
        with c2:
            st.markdown("### 📜 Log 8 Data Terakhir")
            if data_exists: st.table(df.tail(8))
            else: st.info("Database Kosong.")

    # --- TAB 2: ANALISIS ---
    with tab_stat:
        if data_exists:
            recent_df = df.tail(150)
            ekor_list = [int(a[-1]) for a in recent_df['Angka'] if a and a[-1].isdigit()]
            if ekor_list:
                hot_e = str(pd.Series(ekor_list).value_counts().idxmax())
                st.markdown(f"""<div class="analisis-box">
                <p style="color: #FFD700; font-size: 20px;">🔥 EKOR SAKTI SAAT INI: {hot_e}</p>
                <p>Analisis berdasarkan {len(df)} data yang tersimpan.</p>
                </div>""", unsafe_allow_html=True)
                st.plotly_chart(px.bar(x=list(range(10)), y=[ekor_list.count(i) for i in range(10)], title="Tren Frekuensi Angka", color_discrete_sequence=['#FFD700']), use_container_width=True)

    # --- TAB 3: PREDIKSI ULTIMATE V6 ---
    with tab_pred:
        st.subheader("🔮 Generator Prediksi Kompleks")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            mode_p = st.selectbox("Pilih Tipe:", ["5D", "4D", "3D", "2D"])
            jml_p = st.slider("Jumlah Urutan:", 1, 20, 7)
        
        if st.button("🚀 GENERATE PREDIKSI V6"):
            if data_exists:
                # LOGIKA V6: Ambil 5 angka terakhir sebagai pondasi
                last_result = df['Angka'].iloc[-1]
                base_nums = list(set([int(x) for x in last_result if x.isdigit()]))
                master_nums = [0, 2, 3, 5, 8]
                
                # Racikan kolam angka (Weighted Pool)
                pool = base_nums * 4 + master_nums * 2 + [7, 9]
                
                hasil_prediksi = []
                for _ in range(jml_p):
                    random.shuffle(pool)
                    res = "".join([str(x) for x in pool[:int(mode_p[0])]])
                    hasil_prediksi.append(res)
                
                st.markdown("### 🎯 Hasil Tembakan Jitu:")
                for i, h in enumerate(hasil_prediksi, 1):
                    st.markdown(f"**Urutan {i}:** `{h}`")
            else:
                st.warning("Input data dulu di Data Center!")

    # --- TAB 4: BBFS PRO V6 ---
    with tab_bbfs:
        st.subheader("🎲 Sistem BBFS 5D & Poltar")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            angka_main = st.text_input("Masukkan Angka Main (Bebas):", value="02789")
            target_b = st.multiselect("Target Output:", ["5D", "4D", "3D", "2D"], default=["5D", "4D"])
        
        if st.button("🔥 GENERATE BBFS V6"):
            if len(angka_main) >= 2:
                # BBFS 5D Rekomendasi
                st.markdown('<div class="bbfs-box">', unsafe_allow_html=True)
                st.markdown(f"💰 **REKOMENDASI BBFS 5D:** <span class='highlight-gold'>{' - '.join(list(angka_main[:5]))}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Kombinasi berdasarkan target
                for t in target_b:
                    st.write(f"**Pola Tarung {t}:**")
                    combos = list(itertools.permutations(angka_main, int(t[0])))
                    hasil_b = ["".join(p) for p in combos]
                    random.shuffle(hasil_b)
                    st.code(", ".join(hasil_b[:20])) # Tampilkan 20 baris terkuat
            else:
                st.error("Masukkan minimal 2 angka!")

    if st.sidebar.button("🔒 Logout"):
        del st.session_state["password_correct"]; st.rerun()

except Exception as e:
    st.error(f"Sistem Error: {e}")
