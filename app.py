import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import itertools
import random
from datetime import datetime

# Setingan Dasar agar Ringan di HP
st.set_page_config(page_title="RNG System Pro", layout="centered")

# CSS Sederhana agar tampilan tombol bagus di HP
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; }
    .main-header { text-align: center; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Database (Data akan tersimpan selama aplikasi berjalan)
if "db_rizky" not in st.session_state:
    st.session_state.db_rizky = pd.DataFrame(columns=["Waktu", "Sesi", "Tipe", "Angka"])

st.markdown("<h1 class='main-header'>🎯 RNG System Pro</h1>", unsafe_allow_html=True)

# Navigasi Menu Menggunakan TAB (Sangat ringan untuk HP)
menu = st.tabs(["📈 TREN & INPUT", "🔮 MENU PREDIKSI", "🎲 BBFS SMART"])

# --- TAB 1: INPUT & GRAFIK ---
with menu[0]:
    st.subheader("Catat Result & Lihat Grafik")
    with st.expander("➕ Tambah Result Baru"):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.selectbox("Sesi Jam", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"])
        angka_in = st.text_input("Masukkan Angka Keluar (Contoh: 1234)")
        if st.button("Simpan Data"):
            if angka_in:
                new_data = {"Waktu": str(tgl), "Sesi": jam, "Tipe": "RESULT", "Angka": int(angka_in)}
                st.session_state.db_rizky = pd.concat([st.session_state.db_rizky, pd.DataFrame([new_data])], ignore_index=True)
                st.success("Data Berhasil Tersimpan!")

    # Tampilan Grafik
    df_res = st.session_state.db_rizky[st.session_state.db_rizky['Tipe'] == "RESULT"]
    if not df_res.empty:
        fig = go.Figure(go.Scatter(x=df_res['Waktu'], y=df_res['Angka'], mode='lines+markers', line=dict(color='red', width=3)))
        fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data. Silakan input angka keluar pertama kamu!")

# --- TAB 2: MENU PREDIKSI MANDIRI ---
with menu[1]:
    st.subheader("🔮 Prediksi Angka Selanjutnya")
    col1, col2 = st.columns(2)
    with col1:
        tgl_p = st.date_input("Tanggal Target", datetime.now(), key="p_tgl")
    with col2:
        jam_p = st.selectbox("Sesi Target", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"], key="p_jam")
    
    st.write("---")
    if st.button("PROSES PREDIKSI SEKARANG"):
        # Logika Prediksi Sederhana
        hasil_p = random.randint(1000, 9999)
        st.markdown(f"""
            <div style="background-color:#262730; padding:20px; border-radius:15px; text-align:center; border: 2px solid #00FF00;">
                <h3 style="color:white; margin:0;">PREDIKSI SESI {jam_p}</h3>
                <h1 style="color:#00FF00; font-size:55px; margin:10px 0;">{hasil_p}</h1>
                <p style="color:#AAAAAA; margin:0;">Target Tanggal: {tgl_p}</p>
            </div>
        """, unsafe_allow_
