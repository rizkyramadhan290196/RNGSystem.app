import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import collections
import random
import json
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="RIZKY V18 - REBOUND ENGINE", layout="wide")

# --- 1. KONEKSI DATABASE (STABLE) ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f:
            info = json.load(f)
        creds = Credentials.from_service_account_info(info, scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Database_RNG_Rizky")
    except Exception as e:
        st.error(f"Koneksi Gagal: {e}")
        return None

db = init_connection()

# --- 2. ENGINE V18 (LOGIKA PEMULIHAN) ---
def v18_engine(all_res):
    if not all_res: return "012458", {}
    
    scores = {str(i): 0 for i in range(10)}
    last_res = str(all_res[-1])
    
    # A. PENALTI REPEAT (Jangan pasang angka yang baru kembar)
    if len(last_res) >= 2 and last_res[-1] == last_res[-2]:
        scores[last_res[-1]] -= 12.0
        
    # B. GHOST HUNTING (Angka 0, 1, 2 wajib masuk radar)
    scores['0'] += 15.0  # Ghost Utama
    scores['1'] += 10.0  # Ghost Pendamping
    scores['2'] += 8.0
    
    # C. BALANCE FACTOR (Tarik ke angka kecil karena barusan angka besar)
    for i in range(5): # Angka 0-4
        scores[str(i)] += 6.0
        
    # D. DIVERSITY (Cek frekuensi 30 sesi)
    freq = collections.Counter("".join([str(x) for x in all_res[-30:]]))
    for i in range(10):
        scores[str(i)] += (30 - freq.get(str(i), 0)) * 0.3

    bbfs = sorted(scores, key=scores.get, reverse=True)[:6]
    return "".join(sorted(bbfs))

# --- 3. UI & OUTPUT ---
if db:
    try:
        ws = db.worksheet("5D")
        df = pd.DataFrame(ws.get_all_records())
        
        st.title("🛡️ RIZKY V18: REBOUND ENGINE")
        st.markdown("---")

        if not df.empty:
            all_res = [str(x) for x in df['Angka'].tolist()]
            bbfs_v18 = v18_engine(all_res)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.info(f"### 🛡️ BBFS REBOUND\n# {bbfs_v18}")
                st.write("Fokus: Angka Kecil (0, 1, 2) & Ghost hunting.")
                
                # Input Manual Data Baru
                new_res = st.text_input("Input Result Terbaru:")
                if st.button("UPDATE & ANALISIS"):
                    if new_res:
                        ws.append_row([str(datetime.now().date()), new_res])
                        st.success("Data masuk! Menghitung ulang...")
                        st.rerun()

            with col2:
                st.write("### 🎯 SNIPER RECOVERY (ANTI-TWIN GUARD)")
                # Generate 7 Line Sniper
                snipers = []
                # Pastikan angka 0 dan 1 selalu ikut di sniper
                ghosts = [bbfs_v18[0], bbfs_v18[1]] 
                
                while len(snipers) < 7:
                    others = random.sample([x for x in bbfs_v18 if x not in ghosts], 2)
                    line_list = ghosts + others
                    random.shuffle(line_list)
                    line = "".join(line_list)
                    if line[2] != line[3] and line not in snipers:
                        snipers.append(line)
                
                # Tampilan Line
                for i in range(0, len(snipers), 2):
                    c1, c2 = st.columns(2)
                    c1.button(f"LINE {i+1}: {snipers[i]}", use_container_width=True)
                    if i+1 < len(snipers):
                        c2.button(f"LINE {i+2}: {snipers[i+1]}", use_container_width=True)

        st.warning("⚠️ Strategi: Gunakan sistem bet bertingkat. Jangan langsung all-in setelah JP patah.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.error("Koneksi Database Mati. Periksa File JSON kamu!")
