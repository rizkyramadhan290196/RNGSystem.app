import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import itertools
import random
from datetime import datetime

# Konfigurasi dasar
st.set_page_config(page_title="RNG Pro", layout="centered")

# Inisialisasi Database
if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])

st.title("🎯 RNG System Pro")

# Navigasi Menu menggunakan Tab
tab1, tab2, tab3 = st.tabs(["📊 INPUT & TREN", "🔮 PREDIKSI", "🎲 BBFS"])

with tab1:
    st.subheader("Input Result")
    with st.expander("Tambah Data"):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.selectbox("Sesi", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"])
        angka_in = st.text_input("Angka Keluar")
        if st.button("Simpan"):
            if angka_in:
                new_row = {"Waktu": str(tgl), "Sesi": jam, "Angka": int(angka_in)}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Tersimpan!")
    
    if not st.session_state.db.empty:
        fig = go.Figure(go.Scatter(x=st.session_state.db['Waktu'], y=st.session_state.db['Angka'], mode='lines+markers'))
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Menu Prediksi")
    p_jam = st.selectbox("Pilih Jam Target", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"])
    if st.button("Lihat Prediksi"):
        hasil = random.randint(1000, 9999)
        st.info(f"Prediksi Sesi {p_jam}:")
        st.header(f"👉 {hasil}")

with tab3:
    st.subheader("Generator BBFS")
    bbfs = st.text_input("Input Angka")
    if st.button("Generate 10 Line"):
        if bbfs:
            digits = list(bbfs)
            res = [''.join(p) for p in itertools.permutations(digits, 2)]
            random.shuffle(res)
            st.write(", ".join(res[:10]))

st.write("---")
if st.button("Reset Data"):
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])
    st.rerun()
