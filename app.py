import streamlit as st
import pandas as pd
import collections
import random

# --- ENGINE V17: THE TWIN-ANTIDOTE ---
# Fokus: Melawan Twin-Trap & Memaksa Ghost 8 Keluar

def v17_engine(all_res):
    scores = {str(i): 0 for i in range(10)}
    last_res = all_res[-1]
    
    # 1. Twin Guard Logic: Jika ada twin di belakang, kurangi bobotnya
    if last_res[-1] == last_res[-2]:
        scores[last_res[-1]] -= 5.0 
    
    # 2. Ghost Factor: Angka 8 yang tertunda
    scores['8'] += 10.0 
    
    # 3. Analisis Frekuensi (History 20 Sesi)
    freq = collections.Counter("".join(all_res[-20:]))
    for i in range(10):
        scores[str(i)] += (20 - freq.get(str(i), 0)) * 0.5
        
    # 4. Ambil 6 Digit Terbaik
    bbfs = sorted(scores, key=scores.get, reverse=True)[:6]
    return "".join(sorted(bbfs)), scores

# --- UI SNIPER V17 ---
# (Struktur ini bisa kamu ganti di kodingan sebelumnya)
st.subheader("🎯 V17 TWIN-ANTIDOTE ACTIVATED")
bbfs, scores = v17_engine(all_res)
st.success(f"### 🛡️ BBFS ANTI-TWIN: {bbfs}")
st.info("Sistem mendeteksi angka 8 sebagai 'Hantu Utama' dengan bobot tertinggi.")

# Sniper Line Khusus (Anti-Twin)
snipers = []
for _ in range(7):
    line = "".join(random.sample(bbfs, 4))
    if line[2] != line[3]: # Memastikan 2 digit terakhir bukan Twin
        snipers.append(line)
