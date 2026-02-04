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
st.set_page_config(page_title="RIZKY RNG ULTIMATE V5.3 GOLD", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1a1a; color: #FFD700; border-radius: 10px 10px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black; font-weight: bold; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 45px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4);
    }
    .analisis-box {
        padding: 20px; border-radius: 15px; background: #111; 
        border: 1px solid #FFD700; margin: 10px 0;
    }
    .rekomendasi-angka {
        font-size: 24px; color: #FFD700; font-weight: bold; text-align: center;
        background: #222; padding: 10px; border-radius: 10px; border: 1px solid #FFD700;
        margin: 10px 0;
    }
    .status-sinyal {
        font-size: 14px; text-align: center; color: #888; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔐 RIZKY GOLDEN SYSTEM ACCESS</h3>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1])
    with col_l:
        pwd = st.text_input("Enter Key:", type="password")
        if st.button("UNLOCK"):
            if pwd == PASSWORD_RAHASIA:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("Key Incorrect!")
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

    st.title("🎯 RIZKY RNG ULTIMATE V5.3 GOLD")

    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA", "📊 ANALISIS & REKOMENDASI", "🔮 PREDIKSI", "🎲 BBFS"])

    with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi")
                val = st.text_input("Angka")
                if st.form_submit_button("SAVE DATA"):
                    if jam and val.isdigit():
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Terkunci!"); st.rerun()
            if st.button("🗑️ HAPUS TERAKHIR"):
                sheet.delete_rows(len(all_data)); st.rerun()
        with c2:
            if data_exists: st.table(df.tail(8))

    with tab_stat:
        if data_exists:
            ekor_list = [int(a[-1]) for a in df['Angka'] if a and a[-1].isdigit()]
            if ekor_list:
                counts_ekor = pd.Series(ekor_list).value_counts()
                hot_e = str(counts_ekor.idxmax())
                cold_e = str(counts_ekor.idxmin())
                
                # --- AUTO RECOMMENDATION ---
                st.markdown("### 🧠 HASIL SCAN ALGORITMA")
                
                rec_2d = f"{random.randint(0,9)}{hot_e}"
                rec_3d = f"{random.randint(0,9)}{random.randint(0,9)}{hot_e}"
                rec_4d = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{hot_e}"
                
                # Sinyal Kekuatan Data
                sinyal = "🔴 SINYAL LEMAH (Butuh lebih banyak data)" if len(ekor_list) < 10 else "🟢 SINYAL KUAT (Akurasi Tinggi)"

                st.markdown(f"""
                <div class="analisis-box">
                <p style="color: #FFD700; margin-bottom: 5px;">✅ <b>REKOMENDASI EKOR KUAT (PILIHAN UTAMA):</b></p>
                <div class="rekomendasi-angka">{hot_e}</div>
                
                <p style="color: #FFD700; margin-bottom: 5px;">🎯 <b>REKOMENDASI PAKET JADI (TOP):</b></p>
                <div class="rekomendasi-angka">2D: {rec_2d} | 3D: {rec_3d} | 4D: {rec_4d}</div>
                
                <hr style="border: 0.1px solid #333;">
                <p class="status-sinyal">{sinyal}</p>
                <p style="font-size: 13px; color: #aaa;">💡 <i>Tips: Jika sinyal HIJAU, angka rekomendasi memiliki peluang tembus lebih besar berdasarkan sejarah database.</i></p>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    ganjil = len([x for x in ekor_list if x % 2 != 0]); genap = len([x for x in ekor_list if x % 2 == 0])
                    st.plotly_chart(px.pie(values=[ganjil, genap], names=['Ganjil', 'Genap'], title="⚖️ TREN G/G", color_discrete_sequence=['#FFD700', '#222222']), use_container_width=True)
                with col_b:
                    counts = pd.Series(ekor_list).value_counts().reindex(range(10), fill_value=0)
                    st.plotly_chart(px.bar(x=counts.index, y=counts.values, title="📊 FREKUENSI", color=counts.values, color_continuous_scale='YlOrBr'), use_container_width=True)

    with tab_pred:
        if data_exists:
            ca, cb = st.columns(2)
            tgl_p = ca.date_input("Target Hari", datetime.now() + timedelta(days=1))
            mode = cb.selectbox("Pilih Target:", ["2D", "3D", "4D", "5D"])
            jml = st.number_input("Jumlah Baris:", 1, 120, 25)
            if st.button("🔥 GENERATE"):
                random.seed(int(tgl_p.strftime("%Y%m%d")))
                counts = pd.Series(ekor_list).value_counts().reindex(range(10), fill_value=0)
                hot, cold = str(counts.idxmax()), str(counts.idxmin())
                results = []
                for _ in range(jml):
                    kunci = hot if random.random() < 0.7 else cold
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    results.append(prefix + kunci)
                st.code(", ".join(list(set(results))))

    with tab_bbfs:
        b_in = st.text_input("Input Angka Main")
        if st.button("GENERATE BBFS"):
            if b_in:
                combos = [''.join(p) for p in itertools.permutations(b_in, len(b_in))]
                st.code(", ".join(random.sample(combos, min(len(combos), 25))))

    if st.sidebar.button("🔒 Logout"):
        del st.session_state["password_correct"]; st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
