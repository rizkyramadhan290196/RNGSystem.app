import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="RIZKY RNG V8.6", page_icon="🏆", layout="wide")
PASSWORD_RAHASIA = "rizky77"

# --- 2. DATABASE CONNECTION ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"
@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except Exception as e:
        return None

# --- SECURITY ---
if "password_correct" not in st.session_state:
    st.title("🔐 RIZKY RNG V8.6")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

db = init_conn()

# --- 3. UI ---
st.title("🏆 RIZKY MASTER DASHBOARD V8.6")

if db:
    # INPUT SECTION
    st.subheader("📥 Input Data Baru")
    val = st.text_input("Ketik Angka Result:", placeholder="Contoh: 38828")
    if st.button("SIMPAN DATA"):
        d_count = len(val)
        if d_count in [2,3,4,5]:
            try:
                sheet = db.worksheet(f"{d_count}D")
                sheet.append_row([str(datetime.now().date()), val])
                st.success(f"Data {val} masuk ke laci {d_count}D!")
                st.rerun()
            except:
                st.error(f"Tab {d_count}D tidak ditemukan! Pastikan nama Tab di Google Sheets sudah benar.")
        else: st.warning("Masukkan 2, 3, 4, atau 5 angka!")

    st.divider()

    # ANALISA SECTION
    col1, col2 = st.columns(2)
    
    with col1:
        target = st.radio("Pilih Laci Analisa:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            worksheet = db.worksheet(target)
            data = worksheet.get_all_records()
            if data:
                df = pd.DataFrame(data)
                st.write(f"Data Terakhir {target}:")
                st.dataframe(df.tail(5), use_container_width=True)
                
                # Plot
                fig = px.line(df, y='Angka', title=f"Trend {target}", markers=True)
                fig.update_traces(line_color='#FFD700')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Tab {target} masih kosong.")
        except Exception as e:
            st.error(f"Gagal membaca Tab {target}. Pastikan di Baris 1 ada tulisan 'Tanggal' dan 'Angka'.")

    with col2:
        st.subheader("🔮 Prediksi Top 3")
        if st.button("GENERATE ANGKA JITU"):
            try:
                worksheet = db.worksheet(target)
                data = worksheet.get_all_records()
                if len(data) > 0:
                    all_nums = "".join([str(d['Angka']) for d in data])
                    pool = list(all_nums) + [str(i) for i in range(10)]
                    
                    for i in range(1, 4):
                        random.shuffle(pool)
                        pred = "".join(pool[:int(target[0])])
                        st.code(f"URUTAN {i}: {pred}", language="bash")
                else:
                    st.warning("Butuh minimal 1 data di Google Sheets untuk prediksi.")
            except:
                st.error("Gagal Generate. Isi data dulu di Google Sheets.")
else:
    st.error("Koneksi Google Sheets Error!")
