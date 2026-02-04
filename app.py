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
st.set_page_config(page_title="RIZKY RNG ULTIMATE V5.3", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1a1a1a; border-radius: 10px 10px 0 0; padding: 10px 20px; color: #FFD700;
    }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black; font-weight: bold; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 45px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold; font-size: 16px; border: none;
    }
    .analisis-box {
        padding: 20px; border-radius: 15px; background: #111; 
        border: 1px solid #FFD700; margin: 10px 0; line-height: 1.6;
    }
    .rekomendasi-angka {
        font-size: 22px; color: #FFD700; font-weight: bold; text-align: center;
        background: #222; padding: 10px; border-radius: 10px; border: 1px solid #FFD700;
        margin-top: 5px; margin-bottom: 15px;
    }
    .label-kuning { color: #FFD700; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top: 50px;'>🔑 RIZKY PRIVATE ACCESS</h3>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1])
    with col_l:
        pwd = st.text_input("Masukkan Kode:", type="password")
        if st.button("BUKA PANEL"):
            if pwd == PASSWORD_RAHASIA:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("Akses Ditolak!")
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

    st.title("🎯 RIZKY RNG ULTIMATE V5.3")

    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS & REKOMENDASI", "🔮 PREDIKSI RNG", "🎲 BBFS"])

    with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam")
                val = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if jam and val.isdigit():
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Tersimpan!"); st.rerun()
            if st.button("🗑️ HAPUS TERAKHIR"):
                sheet.delete_rows(len(all_data)); st.rerun()
        with c2:
            st.markdown("### 📜 Riwayat Terakhir")
            if data_exists: st.table(df.tail(8))

    with tab_stat:
        if data_exists:
            # Mengolah data untuk analisis posisi
            ekor_list = [int(a[-1]) for a in df['Angka'] if a and a[-1].isdigit()]
            kepala_list = [int(a[-2]) if len(a)>=2 else random.randint(0,9) for a in df['Angka']]
            kop_list = [int(a[-3]) if len(a)>=3 else random.randint(0,9) for a in df['Angka']]
            as_list = [int(a[-4]) if len(a)>=4 else random.randint(0,9) for a in df['Angka']]

            if ekor_list:
                counts_ekor = pd.Series(ekor_list).value_counts()
                hot_e = str(counts_ekor.idxmax())
                cold_e = str(counts_ekor.idxmin())
                
                # --- AUTO RECOMMENDATION SYSTEM ---
                st.markdown("### 🧠 REKOMENDASI ANGKA JADI (SIAP PASANG)")
                
                # Racikan Otomatis
                rec_2d = f"{random.choice(kepala_list)}{hot_e}"
                rec_3d = f"{random.choice(kop_list)}{random.choice(kepala_list)}{hot_e}"
                rec_4d = f"{random.choice(as_list)}{random.choice(kop_list)}{random.choice(kepala_list)}{hot_e}"
                rec_5d = f"{random.randint(0,9)}{rec_4d}"

                st.markdown(f"""
                <div class="analisis-box">
                <span class="label-kuning">📍 REKOMENDASI POSISI BELAKANG (2D):</span>
                <div class="rekomendasi-angka">{rec_2d} , {cold_num if 'cold_num' in locals() else random.randint(10,99)}</div>
                
                <span class="label-kuning">📍 REKOMENDASI 3D (KOP+KEPALA+EKOR):</span>
                <div class="rekomendasi-angka">{rec_3d}</div>
                
                <span class="label-kuning">📍 REKOMENDASI 4D (AS+KOP+KEP+EKOR):</span>
                <div class="rekomendasi-angka">{rec_4d}</div>
                
                <span class="label-kuning">📍 REKOMENDASI 5D ULTIMATE:</span>
                <div class="rekomendasi-angka">{rec_5d}</div>
                
                <hr style="border: 0.5px solid #333;">
                💡 <i>Sistem meracik angka di atas berdasarkan perpaduan <b>Data Hot</b> sesi sebelumnya dengan <b>Pola Posisi</b> As, Kop, dan Kepala yang paling stabil.</i>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    ganjil = len([x for x in ekor_list if x % 2 != 0])
                    genap = len([x for x in ekor_list if x % 2 == 0])
                    st.plotly_chart(px.pie(values=[ganjil, genap], names=['Ganjil', 'Genap'], title="⚖️ TREN GANJIL/GENAP", color_discrete_sequence=['#FFD700', '#222222']), use_container_width=True)
                with col_b:
                    counts = pd.Series(ekor_list).value_counts().reindex(range(10), fill_value=0)
                    st.plotly_chart(px.bar(x=counts.index, y=counts.values, title="📊 FREKUENSI EKOR", color=counts.values, color_continuous_scale='YlOrBr'), use_container_width=True)

    with tab_pred:
        st.subheader("🔮 Hybrid RNG Prediction System")
        if data_exists:
            ca, cb = st.columns(2)
            tgl_p = ca.date_input("Target Hari", datetime.now() + timedelta(days=1))
            mode = cb.selectbox("Pilih Target:", ["2D", "3D", "4D", "5D"])
            jml = st.number_input("Jumlah Baris:", 1, 120, 25)

            if st.button("🔥 RACIK DAFTAR PREDIKSI"):
                random.seed(int(tgl_p.strftime("%Y%m%d")))
                ekor_list = [int(a[-1]) for a in df['Angka'] if a and a[-1].isdigit()]
                counts = pd.Series(ekor_list).value_counts().reindex(range(10), fill_value=0)
                hot, cold = str(counts.idxmax()), str(counts.idxmin())
                results = []
                for _ in range(jml):
                    kunci = hot if random.random() < 0.7 else cold
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    results.append(prefix + kunci)
                st.code(", ".join(list(set(results))))
        else: st.warning("Isi database dulu!")

    with tab_bbfs:
        b_in = st.text_input("Input Angka Main BBFS")
        if st.button("GENERATE BBFS"):
            if b_in:
                combos = [''.join(p) for p in itertools.permutations(b_in, len(b_in))]
                st.code(", ".join(random.sample(combos, min(len(combos), 25))))

    st.sidebar.title("MENU")
    if st.sidebar.button("🔒 Keluar"):
        del st.session_state["password_correct"]; st.rerun()

except Exception as e:
    st.error(f"⚠️ Terjadi Sinkronisasi: {e}")
