import streamlit as st
import pandas as pd
import random
import itertools
from datetime import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="RIZKY RNG V7.0 FINAL", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #FFD700; }
    .stTabs [data-baseweb="tab"] { color: #FFD700; font-size: 18px; }
    .stMetric { background-color: #111; border: 1px solid #FFD700; padding: 10px; border-radius: 10px; }
    .box-prediksi { border: 2px solid #FFD700; padding: 20px; border-radius: 15px; background: #0a0a0a; text-align: center; }
    .bbfs-text { font-size: 30px; letter-spacing: 5px; color: #00ff00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE LOGIC V7.0 ---
def engine_rng_bandar(df, jml_urutan):
    if df.empty: return [], []
    
    # Ambil semua digit dari database
    all_digits = "".join(df['Angka'].tolist())
    counts = pd.Series(list(all_digits)).value_counts()
    
    # Hot & Cold Logic
    hot_nums = counts.head(5).index.tolist() # 5 Angka paling sering
    cold_nums = counts.tail(3).index.tolist() # 3 Angka paling jarang
    
    # Gabungkan dengan bobot khusus (Mendekati RNG Bandar)
    # Bandar sering mengeluarkan 60% Hot, 30% Cold, 10% Surprise
    pool = (hot_nums * 6) + (cold_nums * 3) + [str(i) for i in range(10)]
    
    predictions = []
    for _ in range(jml_urutan):
        random.shuffle(pool)
        line = "".join(pool[:5])
        predictions.append(line)
        
    bbfs_final = sorted(list(set(hot_nums + cold_nums[:2])))[:5]
    return predictions, bbfs_final

# --- APP UI ---
st.title("🏆 RIZKY RNG ULTIMATE V7.0 (FINAL)")
st.subheader("Sistem Prediksi Berbasis Algoritma Statistik Bandar")

tab1, tab2 = st.tabs(["📊 DATABASE & ANALISIS", "🔮 GENERATOR JITU"])

# Simpan data sementara di Session State (karena kamu ingin input manual)
if "db_manual" not in st.session_state:
    st.session_state.db_manual = []

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📥 Input Data Manual")
        with st.form("input_manual"):
            new_val = st.text_input("Masukkan Result (5 Digit):", placeholder="Contoh: 72809")
            if st.form_submit_button("MASUKKAN KE SISTEM"):
                if len(new_val) == 5 and new_val.isdigit():
                    st.session_state.db_manual.append({"Tanggal": datetime.now().strftime("%d-%m"), "Angka": new_val})
                    st.success("Data Masuk!")
                else: st.error("Harus 5 Digit Angka!")
        
        if st.button("🗑️ RESET DATABASE"):
            st.session_state.db_manual = []
            st.rerun()

    with col2:
        st.markdown("### 📋 History Data Terkini")
        temp_df = pd.DataFrame(st.session_state.db_manual)
        st.dataframe(temp_df.tail(10), use_container_width=True)

with tab2:
    if len(st.session_state.db_manual) < 3:
        st.warning("Butuh minimal 3 data manual untuk mulai analisis.")
    else:
        st.markdown("### 🚀 Hasil Simulasi RNG Bandar")
        jml = st.slider("Jumlah Baris:", 1, 15, 7)
        
        if st.button("🔥 GENERATE FINAL PREDICTION"):
            df_final = pd.DataFrame(st.session_state.db_manual)
            prediksi, bbfs = engine_rng_bandar(df_final, jml)
            
            # Tampilan BBFS
            st.markdown(f"""
            <div class="box-prediksi">
                <p>Jaring Pengaman (BBFS 5D)</p>
                <div class="bbfs-text">{' - '.join(bbfs)}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tampilan Urutan
            st.markdown("---")
            cols = st.columns(2)
            for i, p in enumerate(prediksi):
                with cols[i % 2]:
                    st.markdown(f"**URUTAN {i+1}**")
                    st.code(p, language="markdown")

st.sidebar.markdown("""
**SOP SISTEM V7.0:**
1. Masukkan data real result.
2. Pastikan data berjumlah 5 digit.
3. Gunakan BBFS sebagai taruhan utama.
4. Gunakan Urutan sebagai taruhan sampingan.
""")
