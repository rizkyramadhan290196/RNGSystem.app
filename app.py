import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
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
    .mode-invest { background:#001220; border:2px solid #00FF00; padding:15px; border-radius:10px; text-align:center; margin-bottom:10px; }
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
        n = [int(d) for d in str(result_str) if d.isdigit()]
        if len(n) >= 5:
            as_ekor = (n[0] + n[-1]) % 10
            kop_kep = (n[1] + n[-2]) % 10
            tengah = n[len(n)//2]
            return f"{as_ekor}{kop_kep}{tengah}{as_ekor}"
        return "8338" # Default jika data kurang
    except: return "8338"

def generate_weighted_pool(invest_str, bom_str, history_str):
    # Gabungkan semua, beri bobot lebih pada investasi & BOM
    pool = list(invest_str) * 5 + list(bom_str) * 5 + list(history_str[-30:]) * 1
    # V7 Mistik/Indeks
    mistik_map = {'0':'7','1':'0','7':'0','4':'9','9':'4','5':'8','8':'5','2':'5','3':'8','6':'9'}
    for char in (invest_str + bom_str):
        if char in mistik_map: pool.append(mistik_map[char])
    return [c for c in pool if c.isdigit()]

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
        with c2: a_in = st.text_input("Angka Result:", placeholder="Contoh: 09998")
        if st.button("💾 SIMPAN DATA"):
            if a_in:
                db.worksheet(f"{len(a_in)}D").append_row([str(t_in), a_in])
                st.success("Data Tersimpan!")
                st.rerun()
        st.divider()
        l_cek = st.selectbox("Cek Laci:", ["5D", "4D", "3D", "2D"])
        try:
            ws = db.worksheet(l_cek); df_hist = pd.DataFrame(ws.get_all_records())
            if not df_hist.empty: st.dataframe(df_hist.tail(10), use_container_width=True)
        except: st.info("Laci kosong.")

    with tab3:
        st.subheader("🎯 Sniper AI System V10 PRO")
        cs1, cs2, cs3, cs4 = st.columns(4)
        with cs1: s5 = st.button("🔥 5D")
        with cs2: s4 = st.button("🔥 4D")
        with cs3: s3 = st.button("🔥 3D")
        with cs4: s2 = st.button("🔥 2D")
        
        t_digit = st.session_state.get('v10_digit', 5)
        if s5: t_digit = 5
        if s4: t_digit = 4
        if s3: t_digit = 3
        if s2: t_digit = 2
        st.session_state['v10_digit'] = t_digit
        
        try:
            ws_an = db.worksheet(f"{t_digit}D"); df_an = pd.DataFrame(ws_an.get_all_records())
            res_terakhir = str(df_an['Angka'].iloc[-1]) if not df_an.empty else "09998"
            
            msg, color = deteksi_twin_v9(res_terakhir)
            st.markdown(f'<div style="background:{color}; color:black; padding:10px; border-radius:5px; font-weight:bold; margin-bottom:10px;">{msg}</div>', unsafe_allow_html=True)
            
            hist_str = "".join(df_an['Angka'].astype(str).tolist())
            
            # --- ANTI TANDA TANYA LOGIC ---
            if len(hist_str) >= t_digit:
                r1 = "".join(random.sample(hist_str, t_digit))
                r2 = "".join(random.sample(hist_str, t_digit))
            else:
                r1 = res_terakhir.zfill(t_digit)[:t_digit]
                r2 = res_terakhir[::-1].zfill(t_digit)[:t_digit]
            
            angka_bom_tri = hitung_triangle_v9(res_terakhir)
            st.markdown(f'<div class="mode-invest">🛡️ INVESTASI: {r1} — {r2} | 🔥 BOM TRI: {angka_bom_tri}</div>', unsafe_allow_html=True)
            
            weighted_pool = generate_weighted_pool(r1 + r2, angka_bom_tri, hist_str)
            
            for i in range(1, 6):
                snip_list = []
                while len(snip_list) < 10:
                    random.shuffle(weighted_pool)
                    res_snip = "".join(weighted_pool[:t_digit])
                    if len(res_snip) == t_digit and res_snip not in snip_list:
                        snip_list.append(res_snip)
                
                match_score = sum(1 for n in snip_list if any(c in n for c in angka_bom_tri))
                label = '<div class="recommendation-label">🔥 SLOT HUNTER: REKOMENDASI</div>' if match_score > 6 else ""
                
                st.markdown(f'<div class="slot-box">{label}<div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                grid = '<div class="grid-container">'
                for n in snip_list: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div></div>'
                st.markdown(grid, unsafe_allow_html=True)
        except: st.warning("Silakan input data di Tab 1 terlebih dahulu.")

    with tab4:
        st.subheader("🔄 BBFS Ultra Smart Pangkas V10")
        b_in = st.text_input("Ketik Angka BBFS:", key="bbfs_input")
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1: 
            if st.button("💥 BBFS 5D"): st.session_state['bt'] = 5
        with col_b2:
            if st.button("💥 BBFS 4D"): st.session_state['bt'] = 4
        with col_b3:
            if st.button("💥 BBFS 3D"): st.session_state['bt'] = 3
        with col_b4:
            if st.button("💥 BBFS 2D"): st.session_state['bt'] = 2
        
        bt = st.session_state.get('bt', 2)
        if b_in:
            st.write(f"Target Pangkas: **{bt}D**")
            if st.button(f"✂️ PANGKAS {bt}D JADI 15 LINE"):
                pool_b = [c for c in b_in if c.isdigit()]
                most_common = [item[0] for item in Counter(pool_b).most_common(2)]
                hasil_bbfs = []
                for _ in range(5000):
                    random.shuffle(pool_b)
                    res = "".join(pool_b[:bt])
                    if len(res) == bt and res not in hasil_bbfs:
                        if any(mc in res for mc in most_common):
                            hasil_bbfs.append(res)
                    if len(hasil_bbfs) >= 15: break
                
                grid_p = '<div class="grid-container">'
                for x in hasil_bbfs: grid_p += f'<div class="grid-item" style="background:red; border:1px solid white;">{x}</div>'
                grid_p += '</div>'
                st.markdown(grid_p, unsafe_allow_html=True)

else: st.error("Database Diskonek! Cek File JSON Key.")
