import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import itertools
import random
from datetime import datetime

# Konfigurasi Tampilan Utama
st.set_page_config(page_title="RNG V3 PRO FINAL", layout="centered")

# Style CSS agar tombol merah dan tampilan rapi di HP
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #ff4b4b; color: white; }
    h1, h2, h3 { text-align: center; }
    .pred-box { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #00ff00; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Database
if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])

st.title("🎯 RNG SYSTEM V3 PRO")

tab1, tab2, tab3 = st.tabs(["📊 INPUT DATA", "🔮 PREDIKSI JITU", "🎲 BBFS GENERATOR"])

# --- TAB 1: INPUT DATA (JAM BISA TULIS SENDIRI) ---
with tab1:
    st.subheader("Input Result Keluar")
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Pilih Tanggal", datetime.now())
        # DIUBAH: Sekarang pakai text_input agar jam bisa tulis sendiri (contoh: 21.30)
        jam = st.text_input("Sesi Jam (Bisa tulis sendiri)", placeholder="Contoh: 21.30")
        angka_in = st.text_input("Input Angka Result", placeholder="Contoh: 4567")
        submit = st.form_submit_button("SIMPAN DATA")
        
        if submit:
            if jam and angka_in:
                new_row = {"Waktu": str(tgl), "Sesi": jam, "Angka": int(angka_in)}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Data jam {jam} berhasil disimpan!")
            else:
                st.error("Mohon isi Jam dan Angka!")

    if not st.session_state.db.empty:
        st.write("### Riwayat Data")
        st.dataframe(st.session_state.db.tail(5), use_container_width=True)
        fig = go.Figure(go.Scatter(x=st.session_state.db.index, y=st.session_state.db['Angka'], mode='lines+markers', line=dict(color='red')))
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: PREDIKSI JITU (FIX PILIHAN 2D-5D) ---
with tab2:
    st.subheader("Menu Prediksi Cerdas")
    
    if st.session_state.db.empty:
        st.warning("⚠️ Masukkan data di menu INPUT DATA dulu agar sistem bisa bekerja!")
    else:
        tgl_p = st.date_input("Target Tanggal", datetime.now())
        jam_p = st.text_input("Target Jam", placeholder="Contoh: 22.00")
        # DIPERBAIKI: Pilihan Tipe 2D-5D lebih jelas
        tipe_p = st.selectbox("Pilih Tipe Prediksi", ["2D", "3D", "4D", "5D"])
        jml_p = st.radio("Banyak Line", [10, 20], horizontal=True)
        
        if st.button("🔥 GENERATE PREDIKSI SEKARANG"):
            st.write(f"### Hasil {tipe_p} - {jml_p} Line")
            
            # Logika panjang angka berdasarkan tipe
            panjang = int(tipe_p[0])
            for i in range(1, jml_p + 1):
                low = 10**(panjang-1)
                high = (10**panjang) - 1
                angka_hasil = random.randint(low, high)
                # Tampilan kotak hasil prediksi yang rapi
                st.markdown(f"<div class='pred-box'><b>Line {i}:</b> <span style='color:#00ff00; font-size:20px; font-family:monospace;'>{angka_hasil}</span></div>", unsafe_allow_html=True)

# --- TAB 3: BBFS ---
with tab3:
    st.subheader("Generator BBFS")
    bbfs_in = st.text_input("Input Angka Main (BBFS)")
    tipe_b = st.selectbox("Tipe BBFS", ["2D", "3D", "4D", "5D"])
    jml_b = st.radio("Jumlah Line", [10, 20], horizontal=True)
    
    if st.button("PROSES BBFS"):
        if bbfs_in:
            digit_list = list(bbfs_in)
            n = int(tipe_b[0])
            if len(digit_list) >= n:
                kombinasi = [''.join(p) for p in itertools.permutations(digit_list, n)]
                random.shuffle(kombinasi)
                st.success(f"Hasil {tipe_b}:")
                st.code(", ".join(kombinasi[:jml_b]))
            else:
                st.error(f"Butuh minimal {n} angka!")

st.write("---")
if st.button("🗑️ RESET SISTEM"):
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])
    st.rerun()
