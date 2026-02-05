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
st.set_page_config(page_title="RIZKY RNG V5.4.2 GOLD", page_icon="🚀", layout="wide")

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

    st.title("🎯 RIZKY RNG ULTIMATE V5.4.2")

    # --- PEMBUATAN TAB (Penting agar tidak NameError) ---
    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS", "🔮 PREDIKSI", "🎲 BBFS PRO"])

    # --- TAB 1: DATA CENTER (INPUT & HAPUS) ---
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
            
            st.markdown("---")
            st.subheader("🗑️ Alat Pembersih")
            col_del1, col_del2 = st.columns(2)
            with col_del1:
                if st.button("Hapus Terakhir"):
                    if sheet and len(all_data) > 1:
                        sheet.delete_rows(len(all_data))
                        st.warning("Data terakhir dihapus!")
                        st.rerun()
            with col_del2:
                confirm = st.checkbox("Konfirmasi Reset")
                if confirm:
                    if st.button("HAPUS SEMUA"):
                        if sheet:
                            sheet.resize(rows=1)
                            sheet.resize(rows=100)
                            st.error("DATABASE DIBERSIHKAN!")
                            st.rerun()
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
                jml_data = len(df)
                sinyal = "🟢 SINYAL KUAT" if jml_data > 100 else "🟡 SINYAL SEDANG"
                
                st.markdown(f"""<div class="analisis-box">
                <p style="color: #FFD700;">EKOR SAKTI: {hot_e}</p>
                <p style="text-align: center;">{sinyal} ({jml_data} Data)</p>
                </div>""", unsafe_allow_html=True)
                st.plotly_chart(px.bar(x=list(range(10)), y=[ekor_list.count(i) for i in range(10)], title="Tren Ekor", color_discrete_sequence=['#FFD700']), use_container_width=True)

    # --- TAB 3: PREDIKSI ---
    with tab_pred:
        mode = st.selectbox("Target:", ["2D", "3D", "4D", "5D"])
        if st.button("🔥 GENERATE"):
            res = ["".join([str(random.randint(0,9)) for _ in range(int(mode[0]))]) for _ in range(15)]
            st.code(", ".join(res))

    # --- TAB 4: BBFS ---
    with tab_bbfs:
        b_in = st.text_input("Angka Main")
        b_mode = st.radio("Target:", ["2D", "3D", "4D"], horizontal=True)
        if st.button("GENERATE BBFS"):
            if b_in and len(b_in) >= int(b_mode[0]):
                combos = list(itertools.permutations(b_in, int(b_mode[0])))
                hasil = ["".join(p) for p in combos]
                random.shuffle(hasil)
                st.code(", ".join(hasil[:30]))

    if st.sidebar.button("🔒 Logout"):
        del st.session_state["password_correct"]; st.rerun()

except Exception as e:
    st.error(f"Sistem Error: {e}")
