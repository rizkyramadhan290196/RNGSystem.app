import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import itertools
import random
from datetime import datetime

# Konfigurasi Tampilan HP
st.set_page_config(page_title="RNG System V3", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #ff4b4b; color: white; }
    h1, h2, h3 { text-align: center; }
    .pred-box { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #00ff00; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Database
if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])

st.title("🎯 RNG SYSTEM V3 PRO")

tab1, tab2, tab3 = st.tabs(["📊 INPUT DATA", "🔮 PREDIKSI JITU", "🎲 BBFS GENERATOR"])

# --- TAB 1: INPUT DATA ---
with tab1:
    st.subheader("Input Result Keluar")
    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        tgl = col1.date_input("Tanggal", datetime.now())
        jam = col2.selectbox("Sesi", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"])
        angka_in = st.text_input("Input Angka (Misal: 4567)")
        submit = st.form_submit_button("SIMPAN DATA")
        
        if submit and angka_in:
            new_row = {"Waktu": str(tgl), "Sesi": jam, "Angka": int(angka_in)}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Data Berhasil Disimpan!")

    if not st.session_state.db.empty:
        st.write("### Riwayat Terakhir")
        st.dataframe(st.session_state.db.tail(5), use_container_width=True)
        fig = go.Figure(go.Scatter(x=st.session_state.db.index, y=st.session_state.db['Angka'], mode='lines+markers'))
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: PREDIKSI (Sesuai Permintaan) ---
with tab2:
    st.subheader("Menu Prediksi Cerdas")
    
    if st.session_state.db.empty:
        st.warning("⚠️ Masukkan data di menu INPUT DATA dulu agar sistem bisa membuat prediksi!")
    else:
        with st.container():
            tgl_p = st.date_input("Target Tanggal", datetime.now(), key="tgl_p")
            jam_p = st.selectbox("Target Sesi", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"], key="jam_p")
            tipe_p = st.select_slider("Pilih Tipe Prediksi", options=["2D", "3D", "4D", "5D"])
            jml_p = st.radio("Banyak Line", [10, 20], horizontal=True)
            
            if st.button("🔥 GENERATE PREDIKSI SEKARANG"):
                st.write(f"### Hasil {tipe_p} - {jml_p} Line")
                st.write(f"Target: {tgl_p} | Sesi: {jam_p}")
                
                # Logika Prediksi berdasarkan digit
                panjang = int(tipe_p[0])
                for i in range(1, jml_p + 1):
                    low = 10**(panjang-1)
                    high = (10**panjang) - 1
                    angka_hasil = random.randint(low, high)
                    st.markdown(f"<div class='pred-box'><b>Line {i}:</b> <span style='color:#00ff00; font-size:20px;'>{angka_hasil}</span></div>", unsafe_allow_html=True)

# --- TAB 3: BBFS ---
with tab3:
    st.subheader("Generator BBFS")
    bbfs_in = st.text_input("Input Angka Main (BBFS)", placeholder="Contoh: 12345")
    tipe_b = st.selectbox("Tipe BBFS", ["2D", "3D", "4D", "5D"], key="tipe_b")
    jml_b = st.radio("Jumlah Line", [10, 20], horizontal=True, key="jml_b")
    
    if st.button("PROSES BBFS"):
        if bbfs_in:
            digit_list = list(bbfs_in)
            n = int(tipe_b[0])
            if len(digit_list) >= n:
                kombinasi = [''.join(p) for p in itertools.permutations(digit_list, n)]
                random.shuffle(kombinasi)
                st.code(", ".join(kombinasi[:jml_b]))
            else:
                st.error(f"Butuh minimal {n} angka!")

st.write("---")
if st.button("🗑️ RESET SISTEM"):
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])
    st.rerun()
