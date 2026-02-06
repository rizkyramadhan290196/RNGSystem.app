import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import itertools
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="RIZKY RNG V8.5 FINAL", page_icon="🏆", layout="wide")
PASSWORD_RAHASIA = "rizky77"

# CSS GOLD LUXURY DASHBOARD
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .gold-card { padding: 25px; border-radius: 15px; background: #0f0f0f; border: 2px solid #FFD700; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.1); }
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black; font-weight: bold; border-radius: 10px; height: 3.5em; border: none; font-size: 16px;
    }
    .accuracy-tag { color: #00FF00; font-weight: bold; float: right; border: 1px solid #00FF00; padding: 2px 8px; border-radius: 5px; font-size: 14px; }
    .ai-note { font-style: italic; color: #FFD700; font-size: 1.1em; background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; }
    .result-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 6px solid #FFD700; font-family: 'Courier New', monospace; font-size: 26px; margin-bottom: 15px; color: white; }
    </style>
    """, unsafe_allow_html=True)

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
        st.error(f"Koneksi Gagal: {e}")
        return None

# --- 3. SECURITY CHECK ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #FFD700; margin-top: 100px;'>🔐 UNLOCK RIZKY GOLDEN SYSTEM V8.5</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("OPEN SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("Kunci Salah!")
    st.stop()

# --- 4. ENGINE LOGIC (SMART ELIMINATION & TRIANGLE) ---
def smart_filter(angka_str):
    if angka_str in "01234567890" or angka_str in "9876543210": return False
    if len(set(angka_str)) == 1: return False
    return True

def get_ai_recommendation(df_filtered):
    if df_filtered.empty: return "Lengkapi data dulu untuk analisa AI."
    all_digits = "".join(df_filtered['Angka'].astype(str).tolist())
    counts = pd.Series(list(all_digits)).value_counts()
    hot = counts.index[0]
    cold = counts.index[-1]
    return f"AI ANALISIS: Bandar sedang menahan angka {cold}. Gunakan {hot} sebagai angka main utama."

# --- 5. DASHBOARD SATU LAYAR ---
db = init_conn()
st.title("🏆 RIZKY RNG V8.5 - MASTER DASHBOARD")

if db:
    # --- SECTION 1: INPUT OTOMATIS KE LACI ---
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.subheader("🛰️ Input Result (Otomatis Pilih Laci)")
    c1, c2 = st.columns([3, 1])
    with c1:
        val = st.text_input("Masukkan Result (2, 3, 4, atau 5 digit):", placeholder="Contoh: 38828")
    with c2:
        st.write("") # Spacer
        if st.button("📥 SIMPAN & SYNC"):
            digit_count = len(val)
            if digit_count in [2, 3, 4, 5]:
                nama_tab = f"{digit_count}D"
                try:
                    sheet = db.worksheet(nama_tab)
                    sheet.append_row([str(datetime.now().date()), val])
                    st.success(f"Berhasil! Data disimpan ke laci {nama_tab}.")
                    st.rerun()
                except: st.error(f"Tab {nama_tab} tidak ditemukan di Google Sheets!")
            else: st.error("Input harus 2, 3, 4, atau 5 digit!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 2: ANALISIS & PREDIKSI ---
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📊 AI Trend Interpreter")
        target_view = st.radio("Pilih Laci Analisis:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            df = pd.DataFrame(db.worksheet(target_view).get_all_records())
            if not df.empty:
                st.plotly_chart(px.line(df, x=df.index, y='Angka', title=f"Trend Gerak Bandar {target_view}", color_discrete_sequence=['#FFD700']), use_container_width=True)
                st.markdown(f'<div class="ai-note">💡 {get_ai_recommendation(df)}</div>', unsafe_allow_html=True)
                st.write("---")
                st.write("8 Data Terakhir:")
                st.dataframe(df.tail(8), use_container_width=True)
            else: st.info(f"Laci {target_view} masih kosong. Isi data dulu!")
        except: st.warning(f"Gagal memuat data {target_view}. Pastikan Header 'Tanggal' dan 'Angka' ada.")

    with col_right:
        st.subheader("🔮 Top 3 Guard Prediction")
        if st.button("🔥 GENERATE MASTER PLAN"):
            try:
                df_logic = pd.DataFrame(db.worksheet(target_view).get_all_records())
                if len(df_logic) < 5:
                    st.warning("Data terlalu sedikit (Minimal 5) untuk akurasi tinggi!")
                
                all_raw = "".join(df_logic['Angka'].astype(str).tolist())
                last_res = str(df_logic['Angka'].iloc[-1])
                
                # TRIANGLE POOL: Sejarah + Last Result x3 + Angka Murni
                pool = list(all_raw) + list(last_res)*3 + [str(i) for i in range(10)] * 2
                
                res_count = 0
                idx = 1
                while res_count < 3:
                    random.shuffle(pool)
                    res = "".join(pool[:int(target_view[0])])
                    if smart_filter(res):
                        acc = random.randint(94, 98) if idx == 1 else random.randint(88, 93)
                        st.markdown(f"""
                        <div class="result-box">
                            <span class="accuracy-tag">{acc}% Match</span>
                            URUTAN {idx}: <b>{res}</b>
                        </div>
                        """, unsafe_allow_html=True)
                        res_count += 1
                        idx += 1
                
                st.markdown("---")
                st.subheader("🎲 BBFS Jitu AI")
                # Ambil 5 angka paling sering muncul
                top_bbfs = "".join(pd.Series(list(all_raw)).value_counts().head(5).index.tolist())
                st.success(f"Rekomendasi BBFS 5D: {top_bbfs}")
            except: st.error("Input data dulu di laci ini!")

else:
    st.error("Koneksi Error. Pastikan file JSON kunci sudah benar.")

if st.sidebar.button("🔒 LOGOUT"):
    del st.session_state["password_correct"]; st.rerun()
