import streamlit as st
import pandas as pd
import collections
import random

# --- 1. AMBIL DATA DULU (WAJIB) ---
def get_data():
    try:
        # Asumsikan 'db' sudah di-inisialisasi di awal seperti V15
        ws = db.worksheet("5D")
        return pd.DataFrame(ws.get_all_records())
    except:
        return None

df = get_data()

# --- 2. CEK APAKAH DF ADA ---
if df is not None and not df.empty:
    all_res = [str(x) for x in df['Angka'].tolist()]
    
    # --- LOGIKA V17 ---
    def v17_engine(res_list):
        scores = {str(i): 0 for i in range(10)}
        last_res = str(res_list[-1])
        if len(last_res) >= 2 and last_res[-1] == last_res[-2]:
            scores[last_res[-1]] -= 5.0 
        scores['8'] += 10.0 
        # ... (sisanya logika v17)
        bbfs = sorted(scores, key=scores.get, reverse=True)[:6]
        return "".join(sorted(bbfs))

    bbfs = v17_engine(all_res)
    st.success(f"### BBFS V17: {bbfs}")
    # ... (tampilkan line)
else:
    st.error("Database tidak terbaca. Pastikan file JSON-nya ada di folder yang benar & nama Sheet sesuai!")
