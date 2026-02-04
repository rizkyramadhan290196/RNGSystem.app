import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import itertools
import random
from datetime import datetime

# Konfigurasi Tampilan
st.set_page_config(page_title="RNG System Final", layout="centered")

# CSS agar tombol dan teks besar di HP
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    h1, h2, h3 { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Database Sementara
if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])

st.title("🎯 RNG SYSTEM FINAL")

# Navigasi Tab (Paling Ringan & Stabil)
tab1, tab2, tab3 = st.tabs(["📊 DATA & TREN", "🔮 PREDIKSI 10-20", "🎲 BBFS 2D-5D"])

# --- TAB 1: DATA & TREN ---
with tab1:
    st.subheader("Input Result Baru")
    with st.expander("Klik untuk Tambah Angka"):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.selectbox("Sesi", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"])
        angka_in = st.text_input("Input Angka")
        if st.button("SIMPAN DATA"):
            if angka_in:
                new_row = {"Waktu": str(tgl), "Sesi": jam, "Angka": int(angka_in)}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Berhasil Disimpan!")

    if not st.session_state.db.empty:
        st.write("### Grafik Tren")
        fig = go.Figure(go.Scatter(x=st.session_state.db.index, y=st.session_state.db['Angka'], mode='lines+markers', line=dict(color='orange')))
        fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data untuk ditampilkan.")

# --- TAB 2: PREDIKSI MULTI-LINE ---
with tab2:
    st.subheader("Prediksi Angka Main")
    p_jam = st.selectbox("Sesi Target", ["01:00", "07:00", "13:00", "16:00", "19:00", "22:00"], key="pred_jam")
    p_jml = st.radio("Jumlah Prediksi", [10, 20], horizontal=True)
    
    if st.button("GENERATE PREDIKSI"):
        st.success(f"Daftar {p_jml} Prediksi Sesi {p_jam}:")
        hasil_prediksi = [str(random.randint(1000, 9999)) for _ in range(p_jml)]
        for i, h in enumerate(hasil_prediksi, 1):
            st.markdown(f"**{i}.** {h}")

# --- TAB 3: BBFS LENGKAP (2D-5D) ---
with tab3:
    st.subheader("BBFS Generator")
    bbfs_input = st.text_input("Input Angka Main (BBFS)")
    tipe_d = st.selectbox("Pilih Tipe", ["2D", "3D", "4D", "5D"])
    bbfs_jml = st.radio("Jumlah Line", [10, 20], horizontal=True, key="bbfs_jml")
    
    if st.button("PROSES BBFS"):
        if bbfs_input:
            digit_list = list(bbfs_input)
            n = int(tipe_d[0])
            if len(digit_list) >= n:
                kombinasi = [''.join(p) for p in itertools.permutations(digit_list, n)]
                random.shuffle(kombinasi)
                hasil_akhir = kombinasi[:bbfs_jml]
                st.info(f"Hasil {tipe_d} ({len(hasil_akhir)} Line):")
                st.code(", ".join(hasil_akhir))
            else:
                st.error(f"Minimal butuh {n} angka untuk tipe {tipe_d}!")

st.write("---")
if st.button("🗑️ RESET SEMUA DATA"):
    st.session_state.db = pd.DataFrame(columns=["Waktu", "Sesi", "Angka"])
    st.rerun()
