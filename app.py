import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG ---
st.set_page_config(page_title="RIZKY V10 PRO AI", page_icon="⚔️", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 5px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 4px; padding: 5px; text-align: center; color: #00FF00; font-family: monospace; font-size: 14px; font-weight: bold; }
    .slot-box { background: #001220; border: 2px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 15px; position: relative; }
    .slot-title { color: #FFD700; font-weight: bold; border-bottom: 1px solid #444; margin-bottom: 8px; font-size: 14px; }
    .recommendation-label { position: absolute; top: -10px; right: 10px; background: #FF4B4B; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; height: 3.5em; }
    .mode-invest { background:#001220; border:2px solid #00FF00; padding:15px; border-radius:10px; text-align:center; }
    .mode-bom { background:#4b0000; border:2px solid #FFD700; padding:15px; border-radius:10px; text-align:center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC V10 PRO ---
NAMA_KUNCI = "rng-database-486403-1313e482fc6d.json"

@st.cache_resource
def init_conn():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        with open(NAMA_KUNCI) as f: info = json.load(f)
        gc = gspread.authorize(Credentials.from_service_account_info(info, scopes=scope))
        return gc.open("Database_RNG_Rizky")
    except: return None

def deteksi_twin_v9(res_str):
    res = str(res_str)
    counts = {digit: res.count(digit) for digit in set(res)}
    max_twin = max(counts.values()) if counts else 0
    if max_twin == 2:
        return "⚠️ SINYAL KUNING: Pola ABAB/Twin Biasa terdeteksi!", "#FFD700"
    elif max_twin >= 3:
        return "🚨 SINYAL MERAH: AWAS TWIN GILA!", "#FF4B4B"
    return "✅ SINYAL HIJAU: Arus Bersih Terdeteksi.", "#00FF00"

def hitung_triangle_v9(result_str):
    try:
        n = [int(d) for d in str(result_str)]
        if len(n) >= 5:
            as_ekor = (n[0] + n[4]) % 10
            kop_kep = (n[1] + n[3]) % 10
            tengah = n[2]
            return f"{as_ekor}{kop_kep}{tengah}{as_ekor}"
        return "????"
    except: return "????"

def generate_weighted_pool(invest_str, bom_str, history_str):
    # Gabungkan semua sumber, tapi beri bobot lebih pada Investasi dan BOM
    pool = list(invest_str) * 3 + list(bom_str) * 5 + list(history_str[-20:]) * 1
    # Tambahkan angka Mistik/Bayangan (V7)
    mistik_map = {'0': '7', '1': '0', '7': '0', '4': '9', '9': '4', '5': '8', '8': '5'}
    for char in (invest_str + bom_str):
        if char in mistik_map: pool.append(mistik_map[char])
    return pool

db = init_conn()

if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V10 PRO AI")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATA", "📊 ANALISIS", "🎯 SNIPER AI", "🔄 BBFS"])

    with tab1:
        st.subheader("📥 Input Hasil Result")
        c1, c2 = st.columns(2)
        with c1: t_in = st.date_input("Tanggal:", datetime.now())
        with c2: a_in = st.text_input("Angka Result:", placeholder="Contoh: 94945")
        if st.button("💾 SIMPAN DATA"):
            if a_in:
                db.worksheet(f"{len(a_in)}D").append_row([str(t_in), a_in])
                st.success("Data Tersimpan!")
                st.rerun()

    with tab3:
        st.subheader("🎯 Sniper AI System V10 PRO")
        cs1, cs2, cs3, cs4 = st.columns(4)
        with cs1: s5 = st.button("🔥 5D")
        with cs2: s4 = st.button("🔥 4D")
        with cs3: s3 = st.button("🔥 3D")
        with cs4: s2 = st.button("🔥 2D")
        
        t_digit = st.session_state.get('last_digit_v9', None)
        if s5: t_digit = 5
        if s4: t_digit = 4
        if s3: t_digit = 3
        if s2: t_digit = 2
        
        if t_digit:
            st.session_state['last_digit_v9'] = t_digit
            try:
                ws_an = db.worksheet(f"{t_digit}D"); df_an = pd.DataFrame(ws_an.get_all_records())
                res_terakhir = str(df_an['Angka'].iloc[-1]) if not df_an.empty else "00000"
                msg, color = deteksi_twin_v9(res_terakhir)
                st.markdown(f'<div style="background:{color}; color:black; padding:10px; border-radius:5px; font-weight:bold; margin-bottom:10px;">{msg}</div>', unsafe_allow_html=True)
                
                # --- LOGIKA BOBOT V10 ---
                hist_str = "".join(df_an['Angka'].astype(str).tolist())
                # Simulasi Investasi & BOM (r1, r2, bom)
                random.seed(len(hist_str))
                r1 = "".join(random.sample(hist_str[-50:], t_digit))
                r2 = "".join(random.sample(hist_str[-50:], t_digit))
                angka_bom_tri = hitung_triangle_v9(res_terakhir)
                
                st.markdown(f'<div class="mode-invest">🛡️ INVESTASI: {r1} — {r2} | 🔥 BOM TRI: {angka_bom_tri}</div>', unsafe_allow_html=True)
                
                weighted_pool = generate_weighted_pool(r1 + r2, angka_bom_tri, hist_str)
                
                # --- SLOT HUNTER ENGINE ---
                for i in range(1, 6):
                    label_html = ""
                    # Slot Hunter: Menandai slot yang mengandung angka dari BOM atau Investasi paling banyak
                    snip_list = []
                    while len(snip_list) < 10:
                        random.shuffle(weighted_pool); r = "".join(weighted_pool[:t_digit])
                        if r not in snip_list: snip_list.append(r)
                    
                    # Hitung kecocokan
                    match_score = sum(1 for n in snip_list if any(char in n for char in angka_bom_tri))
                    if match_score > 6:
                        label_html = '<div class="recommendation-label">🔥 SLOT HUNTER: REKOMENDASI</div>'
                    
                    st.markdown(f'<div class="slot-box">{label_html}<div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                    grid = '<div class="grid-container">'
                    for n in snip_list: grid += f'<div class="grid-item">{n}</div>'
                    grid += '</div></div>'
                    st.markdown(grid, unsafe_allow_html=True)
            except: st.error("Lengkapi data!")

    with tab4:
        st.subheader("🔄 BBFS Ultra Smart Pangkas V10")
        b_in = st.text_input("Ketik Angka BBFS:", key="bbfs_input")
        if b_in:
            # Cari angka paling panas untuk filter dinamis
            most_common = [item[0] for item in Counter(b_in).most_common(2)]
            if st.button("✂️ PANGKAS JADI 15 LINE (DINAMIS)"):
                pool_b = list(b_in); hasil_bbfs = []
                for _ in range(1000):
                    temp = pool_b.copy(); random.shuffle(temp); res = "".join(temp[:2]) # Default 2D
                    if res not in hasil_bbfs and any(mc in res for mc in most_common):
                        hasil_bbfs.append(res)
                    if len(hasil_bbfs) >= 15: break
                
                grid_p = '<div class="grid-container">'
                for x in hasil_bbfs: grid_p += f'<div class="grid-item" style="background:red; border:1px solid white;">{x}</div>'
                grid_p += '</div>'; st.markdown(grid_p, unsafe_allow_html=True)
                st.info(f"Pangkas otomatis berdasarkan angka terkuat: {most_common}")

else: st.error("Database Diskonek!")
