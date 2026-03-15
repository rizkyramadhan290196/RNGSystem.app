import streamlit as st
import pandas as pd
import collections
import random

# --- ENGINE V17.1 (STABILIZED) ---
def v17_engine(all_res):
    # Mengatasi jika database kosong
    if not all_res: return "014578", {}
    
    scores = {str(i): 0 for i in range(10)}
    last_res = str(all_res[-1])
    
    # 1. Twin Guard Logic
    if len(last_res) >= 2 and last_res[-1] == last_res[-2]:
        scores[last_res[-1]] -= 5.0 
    
    # 2. Ghost Factor (Angka 8 yang tertunda)
    scores['8'] += 10.0 
    
    # 3. Analisis Frekuensi
    freq = collections.Counter("".join([str(x) for x in all_res[-20:]]))
    for i in range(10):
        scores[str(i)] += (20 - freq.get(str(i), 0)) * 0.5
        
    bbfs = sorted(scores, key=scores.get, reverse=True)[:6]
    return "".join(sorted(bbfs)), scores

# --- MAIN APP FLOW ---
# Pastikan data terambil sebelum fungsi dipanggil
if 'df' in locals() or 'df' in globals():
    all_res = [str(x) for x in df['Angka'].tolist()]
    
    st.subheader("🎯 V17 TWIN-ANTIDOTE ACTIVATED")
    bbfs, scores = v17_engine(all_res)
    
    st.success(f"### 🛡️ BBFS ANTI-TWIN: {bbfs}")
    st.info("Sistem mendeteksi angka 8 sebagai 'Hantu Utama' dengan bobot tertinggi.")

    # Sniper Line Khusus (Anti-Twin)
    snipers = []
    while len(snipers) < 7:
        line = "".join(random.sample(list(bbfs), 4))
        # Pastikan tidak ada twin di ekor
        if line[2] != line[3]: 
            snipers.append(line)
            
    st.write("### 🎯 7 Line Sniper Anti-Twin:")
    cols = st.columns(4)
    for i, val in enumerate(snipers):
        cols[i % 4].markdown(f"**{val}**")
else:
    st.error("Database tidak terbaca. Pastikan koneksi Sheets aktif!")
