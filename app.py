import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import itertools
import random

# --- 1. SETTINGS & PASSWORD ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY RNG V5.4.1 GOLD", page_icon="🚀", layout="wide")

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
    .status-teks { text-align: center; font-size: 14px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔐 RIZKY GOLDEN SYSTEM ACCESS</h3>", unsafe_allow_html=True)
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

try:
    sheet = init_conn()
    all_data = sheet.get_all_values()
    df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
    df['Angka'] = df['Angka'].astype(str).str.strip()
    data_exists = not df.empty

    st.title("🎯 RIZKY RNG ULTIMATE V5.4.1")

    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS", "🔮 PREDIKSI", "🎲 BBFS PRO"])

    with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            target = st.selectbox("Pilih Pasaran:", ["TTM 5D", "TTM 4D", "KINGKONG 4D"])
            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam", value=target)
                val = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if val.isdigit():
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Tersimpan!"); st.rerun()
            if st.button("🗑️ HAPUS TERAKHIR"):
                sheet.delete_rows(len(all_data)); st.rerun()
        with c2:
            st.markdown("### 📜 Log 8 Data Terakhir")
            if data_exists: st.table(df.tail(8))

    with tab_stat:
        if data_exists:
            # OPTIMASI: Hanya fokus 150 sesi terakhir untuk pola terbaru
            recent_df = df.tail(150)
            ekor_list = [int(a[-1]) for a in recent_df['Angka'] if a and a[-1].isdigit()]
            
            if ekor_list:
                counts_ekor = pd.Series(ekor_list).value_counts()
                hot_e = str(counts_ekor.idxmax())
                
                # Logika Sinyal 3 Warna
                jml_data = len(df)
                if jml_data < 50:
                    sinyal, pesan = "🔴", "SINYAL LEMAH (Butuh lebih banyak data)"
                elif jml_data < 150:
                    sinyal, pesan = "🟡", "SINYAL SEDANG (Mulai Stabil)"
                else:
                    sinyal, pesan = "🟢", "SINYAL KUAT (Akurasi Tinggi)"

                rec_2d = f"{random.randint(0,9)}{hot_e}"
                rec_3d = f"{random.randint(0,9)}{random.randint(0,9)}{hot_e}"
                rec_4d = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{hot_e}"
                rec_5d = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{hot_e}"

                st.markdown(f"""
                <div class="analisis-box">
                <p style="color: #FFD700;">✅ <b>HASIL SCAN 150 SESI TERAKHIR:</b></p>
                <div class="rekomendasi-angka" style="font-size: 35px;">EKOR SAKTI: {hot_e}</div>
                <p style="color: #FFD700; margin-top: 15px;">🎯 <b>PAKET REKOMENDASI:</b></p>
                <div class="rekomendasi-angka">
                    2D: {rec_2d} | 3D: {rec_3d}<br>
                    4D: {rec_4d} | 5D: {rec_5d}
                </div>
                <hr style="border: 0.1px solid #333;">
                <p class="status-teks">{sinyal} {pesan} (Total: {jml_data} Data)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.plotly_chart(px.bar(x=list(range(10)), y=[ekor_list.count(i) for i in range(10)], 
                                     title="Grafik Frekuensi Ekor (Tren Terbaru)", color_discrete_sequence=['#FFD700']), use_container_width=True)

    with tab_pred:
        if data_exists:
            mode = st.selectbox("Pilih Target:", ["2D", "3D", "4D", "5D"])
            jml = st.number_input("Jumlah Baris:", 1, 100, 20)
            if st.button("🔥 GENERATE PREDIKSI"):
                # Prediksi berdasarkan Ekor Sakti
                ekor_list = [int(a[-1]) for a in df.tail(150)['Angka'] if a and a[-1].isdigit()]
                hot = str(pd.Series(ekor_list).value_counts().idxmax())
                results = []
                for _ in range(jml):
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    results.append(prefix + hot)
                st.code(", ".join(list(set(results))))

    with tab_bbfs:
        st.subheader("🎲 BBFS GENERATOR PRO")
        b_in = st.text_input("Masukkan Angka Main (Contoh: 12345)")
        b_mode = st.radio("Pilih Target:", ["2D", "3D", "4D"], horizontal=True)
        if st.button("GENERATE KOMBINASI"):
            if b_in and len(b_in) >= int(b_mode[0]):
                combos = list(itertools.permutations(b_in, int(b_mode[0])))
                hasil = ["".join(p) for p in combos]
                random.shuffle(hasil)
                st.code(", ".join(hasil[:30])) # Menampilkan 30 kombinasi acak
            else:
                st.warning(f"Masukkan minimal {b_mode[0]} digit!")

    if st.sidebar.button("🔒 Logout"):
        del st.session_state["password_correct"]; st.rerun()

except Exception as e:
    st.error(f"Sistem Error: {e}")
