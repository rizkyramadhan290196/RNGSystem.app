import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import itertools
import random

# --- 1. SETTINGS ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY RNG ULTIMATE V5", page_icon="🔥", layout="wide")

# CSS LUXURY GOLD THEME
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
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
    }
    .stTable { background-color: #111; border-radius: 10px; }
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

    st.title("🎯 RIZKY RNG ULTIMATE V5.0")

    tab_db, tab_stat, tab_pred, tab_bbfs = st.tabs(["📥 DATA CENTER", "📊 ANALISIS SAKTI", "🔮 PREDIKSI RNG", "🎲 BBFS"])

    with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam (Contoh: SGP 17.00)")
                val = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if jam and val.isdigit():
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Data Berhasil Dikunci!"); st.rerun()
            if st.button("🗑️ HAPUS BARIS TERAKHIR"):
                sheet.delete_rows(len(all_data)); st.rerun()
        with c2:
            st.markdown("### 📜 10 Riwayat Terakhir")
            if data_exists: st.table(df.tail(10))

    with tab_stat:
        if data_exists:
            # Mengambil ekor
            ekor_list = [int(a[-1]) for a in df['Angka'] if a and a[-1].isdigit()]
            
            if ekor_list:
                col_a, col_b = st.columns(2)
                
                ganjil = len([x for x in ekor_list if x % 2 != 0])
                genap = len([x for x in ekor_list if x % 2 == 0])
                kecil = len([x for x in ekor_list if x <= 4])
                besar = len([x for x in ekor_list if x >= 5])

                with col_a:
                    fig_gg = px.pie(values=[ganjil, genap], names=['Ganjil', 'Genap'], 
                                   title="⚖️ TREN GENAP/GANJIL",
                                   color_discrete_sequence=['#FFD700', '#222222']) # Gold & Black
                    fig_gg.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_gg, use_container_width=True)
                
                with col_b:
                    fig_bk = px.pie(values=[kecil, besar], names=['Kecil (0-4)', 'Besar (5-9)'], 
                                   title="📏 TREN BESAR/KECIL",
                                   color_discrete_sequence=['#B8860B', '#444444']) # Bronze & Dark Grey
                    fig_bk.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_bk, use_container_width=True)

                # Frekuensi Bar Chart
                counts = pd.Series(ekor_list).value_counts().reindex(range(10), fill_value=0)
                fig_bar = px.bar(x=counts.index, y=counts.values, 
                                 title="📊 FREKUENSI DIGIT TERAKHIR",
                                 labels={'x':'Digit', 'y':'Jumlah Keluar'},
                                 color=counts.values, color_continuous_scale='YlOrBr')
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_bar, use_container_width=True)
            else: st.info("Tambahkan data angka untuk melihat statistik.")
        else: st.warning("Database masih kosong!")

    with tab_pred:
        st.subheader("🔮 Hybrid RNG Prediction System")
        if data_exists:
            ca, cb = st.columns(2)
            tgl_p = ca.date_input("Target Hari/Tanggal", datetime.now() + timedelta(days=1))
            mode = cb.selectbox("Pilih Target:", ["2D", "3D", "4D", "5D"])
            jml = st.number_input("Jumlah Baris:", 1, 120, 25)

            if st.button("🔥 RACIK ANGKA SAKTI"):
                # Seed unik berdasarkan tanggal
                random.seed(int(tgl_p.strftime("%Y%m%d")))
                
                # Identifikasi Hot & Cold
                ekor_list = [int(a[-1]) for a in df['Angka'] if a and a[-1].isdigit()]
                counts = pd.Series(ekor_list).value_counts().reindex(range(10), fill_value=0)
                hot = str(counts.idxmax())
                cold = str(counts.idxmin())
                
                results = []
                for _ in range(jml):
                    # Campuran 70% Hot, 30% Cold
                    kunci = hot if random.random() < 0.7 else cold
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    results.append(prefix + kunci)
                
                st.markdown(f"### 📅 Prediksi {mode} Untuk {tgl_p.strftime('%d-%m-%Y')}")
                st.code(", ".join(list(set(results))))
                st.success(f"Analisis: Kunci Utama ({hot}), Kunci Cadangan ({cold})")
        else: st.warning("Sistem membutuhkan data di Data Center untuk merumus!")

    with tab_bbfs:
        st.subheader("🎲 BBFS Generator")
        b_in = st.text_input("Input Angka Main (Contoh: 12345)")
        b_jml = st.number_input("Tampilkan Berapa Baris:", 1, 100, 25)
        if st.button("GENERATE BBFS"):
            if b_in:
                combos = [''.join(p) for p in itertools.permutations(b_in, len(b_in))]
                final_bbfs = random.sample(combos, min(len(combos), b_jml))
                st.code(", ".join(final_bbfs))

    # Tombol Logout di Sidebar
    st.sidebar.title("MENU")
    if st.sidebar.button("🔒 Keluar & Kunci"):
        del st.session_state["password_correct"]
        st.rerun()

except Exception as e:
    st.error(f"⚠️ Terjadi Sinkronisasi: {e}")
