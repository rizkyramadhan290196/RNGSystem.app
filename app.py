import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import itertools
import random

# --- 1. PASSWORD & CONFIG ---
PASSWORD_RAHASIA = "rizky77" 
st.set_page_config(page_title="RIZKY SMART RNG V4.5", page_icon="🎯", layout="wide")

# CSS Premium
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNGSI LOGIN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>🔓 AKSES TERKUNCI</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Kode Akses:", type="password")
        if st.button("MASUK"):
            if pwd == PASSWORD_RAHASIA:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ Salah!")
        return False
    return True

if check_password():
    # --- 3. KONEKSI DATABASE ---
    NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"
    
    @st.cache_resource
    def init_connection():
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        with open(NAMA_KUNCI) as f: info_kunci = json.load(f)
        creds = Credentials.from_service_account_info(info_kunci, scopes=scope)
        return gspread.authorize(creds).open("Database_RNG_Rizky").get_worksheet(0)

    try:
        sheet = init_connection()
        all_data = sheet.get_all_values()
        
        if len(all_data) > 1:
            df = pd.DataFrame(all_data[1:], columns=all_data[0])
            df['Angka'] = df['Angka'].astype(str).str.strip()
            data_tersedia = True
        else:
            df = pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
            data_tersedia = False

        st.title("🎯 RIZKY SMART RNG V4.5")

        tab1, tab2, tab3, tab4 = st.tabs(["📥 DATABASE", "📈 GRAFIK", "🔮 PREDIKSI", "🎲 BBFS"])

        # --- TAB 1: DATABASE ---
        with tab1:
            c1, c2 = st.columns([1, 2])
            with c1:
                with st.form("in_v4", clear_on_submit=True):
                    tgl = st.date_input("Tanggal", datetime.now())
                    jam = st.text_input("Jam")
                    angka_in = st.text_input("Hasil Angka")
                    if st.form_submit_button("SIMPAN DATA"):
                        if jam and angka_in:
                            sheet.append_row([str(tgl), jam, str(angka_in)])
                            st.success("Tersimpan!")
                            st.rerun()
                if st.button("🗑️ HAPUS TERAKHIR"):
                    sheet.delete_rows(len(all_data))
                    st.rerun()
            with c2:
                if data_tersedia: st.table(df.tail(8))

        # --- TAB 2: GRAFIK (PERBAIKAN WARNA) ---
        with tab2:
            st.subheader("Statistik Frekuensi Angka")
            if data_tersedia:
                ekor_list = [a[-1] for a in df['Angka'] if a != ""]
                if ekor_list:
                    counts = pd.Series(ekor_list).value_counts().reindex([str(i) for i in range(10)], fill_value=0)
                    # Mengganti Goldenrod dengan 'thermal' yang pasti didukung
                    fig = px.bar(x=counts.index, y=counts.values, 
                                 labels={'x':'Angka Ekor', 'y':'Kali Keluar'},
                                 color=counts.values, color_continuous_scale='thermal')
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig, use_container_width=True)
                else: st.info("Data angka belum lengkap.")
            else: st.warning("Database kosong!")

        # --- TAB 3: PREDIKSI (FITUR TANGGAL) ---
        with tab3:
            st.subheader("🔮 Prediksi Harian")
            col_a, col_b = st.columns(2)
            tgl_pred = col_a.date_input("Untuk Tanggal:", datetime.now() + timedelta(days=1))
            mode = col_b.selectbox("Mode:", ["2D", "3D", "4D", "5D"])
            jml_m = st.number_input("Jumlah Urutan:", min_value=1, value=25)
            
            if st.button("RACIK UNTUK TANGGAL INI"):
                # Seed berdasarkan tanggal agar hasil konsisten tapi unik tiap hari
                random.seed(int(tgl_pred.strftime("%Y%m%d")))
                hot_ekor = df['Angka'].str[-1].mode()[0] if data_tersedia else "7"
                
                hasil = []
                for _ in range(int(jml_m)):
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    hasil.append(prefix + hot_ekor)
                
                st.markdown(f"### 📅 Prediksi {mode} - {tgl_pred.strftime('%d %B %Y')}")
                st.code(", ".join(list(set(hasil))) )
                st.info(f"Analisis berdasarkan Ekor Terkuat: {hot_ekor}")

        # --- TAB 4: BBFS ---
        with tab4:
            b_in = st.text_input("Angka Main")
            b_jml = st.number_input("Total Urutan:", min_value=1, value=25)
            if st.button("PROSES BBFS"):
                if b_in:
                    combos = [''.join(p) for p in itertools.permutations(b_in, len(b_in))]
                    res = random.sample(combos, min(len(combos), b_jml))
                    st.code(", ".join(res))

        if st.sidebar.button("Logout"):
            del st.session_state["password_correct"]
            st.rerun()

    except Exception as e:
        st.error(f"Sinkronisasi: {e}")
