import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import collections
import random
import json
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RIZKY V17 - ANTI ERROR", layout="wide")

# --- 1. KONEKSI DATABASE (FAIL-SAFE) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        # Mencoba membaca file JSON
        with open(NAMA_KUNCI) as f:
            info = json.load(f)
        creds = Credentials.from_service_account_info(info, scopes=scope)
        client = gspread.authorize(creds)
        # Membuka Spreadsheet
        return client.open("Database_RNG_Rizky")
    except Exception as e:
        st.error(f"Gagal Koneksi: {e}")
        return None

db = init_connection()

# --- 2. LOGIKA UTAMA V17 ---
def v17_logic(all_res):
    scores = {str(i): 0 for i in range(10)}
    last_res = str(all_res[-1])
    
    # Twin Guard: Jika ekor kembar, kurangi skor angka tersebut
    if len(last_res) >= 2 and last_res[-1] == last_res[-2]:
        scores[last_res[-1]] -= 5.0 
    
    # Ghost Factor: Angka 8 adalah prioritas (Ghost)
    scores['8'] += 12.0 
    
    # Frekuensi: Angka yang jarang muncul dapat skor lebih
    combined_data = "".join([str(x) for x in all_res[-30:]])
    freq = collections.Counter(combined_data)
    for i in range(10):
        scores[str(i)] += (30 - freq.get(str(i), 0)) * 0.5
        
    bbfs = sorted(scores, key=scores.get, reverse=True)[:6]
    return "".join(sorted(bbfs))

# --- 3. TAMPILAN INTERFACE ---
if db:
    try:
        ws = db.worksheet("5D")
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        
        tab1, tab2 = st.tabs(["📥 INPUT", "🎯 ANALISIS V17"])
        
        with tab1:
            res_in = st.text_input("Input Result (Contoh: 71422):")
            if st.button("SIMPAN DATA"):
                if res_in:
                    ws.append_row([str(datetime.now().date()), res_in])
                    st.success("Data Tersimpan!")
                    st.rerun()

        with tab2:
            if not df.empty:
                all_res = [str(x) for x in df['Angka'].tolist()]
                bbfs_hasil = v17_logic(all_res)
                
                st.success(f"### 🛡️ BBFS ANTI-TWIN: {bbfs_hasil}")
                
                # Generate Sniper
                snipers = []
                while len(snipers) < 7:
                    line = "".join(random.sample(list(bbfs_hasil), 4))
                    if line[2] != line[3]: # Anti-twin ekor
                        snipers.append(line)
                
                st.write("### 🎯 7 LINE SNIPER V17")
                cols = st.columns(4)
                for i, l in enumerate(snipers):
                    cols[i%4].info(f"**{l}**")
            else:
                st.warning("Data di Sheet masih kosong.")
                
    except Exception as e:
        st.error(f"Error Membaca Sheet: {e}. Pastikan nama tab adalah '5D'")
else:
    st.error("Sistem Berhenti. Periksa file JSON dan izin akses Google Sheet.")
