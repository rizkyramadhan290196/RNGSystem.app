import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import random
from collections import Counter

# --- 1. CONFIG ---
st.set_page_config(page_title="RIZKY V11 PRO - DATA 5D PUSAT", page_icon="⚔️", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); gap: 8px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 5px; padding: 10px; text-align: center; color: #00FF00; font-family: monospace; font-size: 16px; font-weight: bold; }
    .slot-box { background: #001220; border: 2px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 15px; position: relative; }
    .slot-title { color: #FFD700; font-weight: bold; border-bottom: 1px solid #444; margin-bottom: 8px; font-size: 14px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; height: 3.5em; background-color: #1a1a1a; color: white; }
    .mode-invest { background:#001220; border:2px solid #00FF00; padding:15px; border-radius:10px; text-align:center; margin-bottom:10px; color: white; }
    .autopick-box { background: linear-gradient(45deg, #4b0082, #000000); border: 2px solid #FFD700; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-top: 20px; box-shadow: 0px 0px 15px #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC CORE ---
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
    if max_twin == 2: return "⚠️ SINYAL KUNING: Pola Twin Biasa!", "#FFD700"
    elif max_twin >= 3: return "🚨 SINYAL MERAH: AWAS TWIN GILA!", "#FF4B4B"
    return "✅ SINYAL HIJAU: Arus Bersih.", "#00FF00"

def hitung_triangle_v11(result_str):
    try:
        n = [int(d) for d in str(result_str) if d.isdigit()]
        if len(n) >= 5:
            v1 = (n[0] + n[2]) % 10
            v2 = (n[1] + n[4]) % 10
            v3 = (n[-1] * 3) % 10 
            return f"{v1}{v2}{v3}{v1}"
        return "7167"
    except: return "7167"

def generate_weighted_pool(invest_str, bom_str, history_str):
    pool = list(invest_str) * 10 + list(bom_str) * 10 + list(history_str[-100:]) * 1
    mistik_map = {'0':'7','1':'0','7':'0','4':'9','9':'4','5':'8','8':'5','2':'5','3':'8','6':'9'}
    for char in (invest_str + bom_str):
        if char in mistik_map: pool.append(mistik_map[char])
    return [c for c in pool if c.isdigit()]

db = init_conn()

# --- 3. UI ---
if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V11 PRO AUTO-PICK")
    pwd = st.text_input("Akses Kunci:", type="password")
    if st.button("UNLOCK SYSTEM"):
        if pwd == PASSWORD_RAHASIA:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

if db:
    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATA", "📊 ANALISIS", "🎯 SNIPER AI", "🔄 BBFS"])

    with tab1:
        st.subheader("📥 Input Hasil Result (Fokus Data 5D)")
        c1, c2 = st.columns(2)
        with c1: t_in = st.date_input("Tanggal:", datetime.now())
        with c2: a_in = st.text_input("Angka Result 5D:", placeholder="Contoh: 91697")
        if st.button("💾 SIMPAN DATA"):
            if a_in:
                db.worksheet("5D").append_row([str(t_in), a_in])
                st.success(f"Data 5D Tersimpan!")
                st.rerun()

    with tab3:
        st.subheader("🎯 Sniper AI (Pusat Data 5D)")
        cs1, cs2, cs3, cs4 = st.columns(4)
        with cs1: 
            if st.button("🔥 5D"): st.session_state['v_digit'] = 5
        with cs2: 
            if st.button("🔥 4D"): st.session_state['v_digit'] = 4
        with cs3: 
            if st.button("🔥 3D"): st.session_state['v_digit'] = 3
        with cs4: 
            if st.button("🔥 2D"): st.session_state['v_digit'] = 2
        
        t_digit = st.session_state.get('v_digit', 2)
        st.info(f"Mode Sniper: **{t_digit}D** | Mengacu pada Data 5D")
        
        try:
            # SEMUA MODE AMBIL DARI DATABASE 5D
            ws_an = db.worksheet("5D")
            df_an = pd.DataFrame(ws_an.get_all_records())
            res_terakhir = str(df_an['Angka'].iloc[-1]) if not df_an.empty else "91697"
            
            msg, color = deteksi_twin_v9(res_terakhir)
            st.markdown(f'<div style="background:{color}; color:black; padding:10px; border-radius:5px; font-weight:bold; margin-bottom:10px; text-align:center;">{msg} | Result Akhir: {res_terakhir}</div>', unsafe_allow_html=True)
            
            hist_str = "".join(df_an['Angka'].astype(str).tolist())
            r1 = "".join(random.sample(hist_str, t_digit)) if len(hist_str) >= t_digit else res_terakhir.zfill(t_digit)[-t_digit:]
            r2 = "".join(random.sample(hist_str, t_digit)) if len(hist_str) >= t_digit else res_terakhir[::-1].zfill(t_digit)[-t_digit:]
            
            angka_bom_tri = hitung_triangle_v11(res_terakhir)[:t_digit]
            st.markdown(f'<div class="mode-invest">🛡️ INVESTASI: {r1} — {r2} | 🔥 BOM TRI: {angka_bom_tri}</div>', unsafe_allow_html=True)
            
            weighted_pool = generate_weighted_pool(r1 + r2, angka_bom_tri, hist_str)
            
            all_generated = []
            for i in range(1, 4):
                snip_list = []
                while len(snip_list) < 10:
                    random.shuffle(weighted_pool)
                    res_snip = "".join(weighted_pool[:t_digit])
                    if len(res_snip) == t_digit:
                        snip_list.append(res_snip)
                        all_generated.append(res_snip)
                
                st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                grid = '<div class="grid-container">'
                for n in snip_list: grid += f'<div class="grid-item">{n}</div>'
                grid += '</div></div>'
                st.markdown(grid, unsafe_allow_html=True)

            st.markdown('<div class="autopick-box">', unsafe_allow_html=True)
            st.markdown(f"### ⚡ RIZKY AUTO-PICK TOP 5 ({t_digit}D)")
            top_picks = [item[0] for item in Counter(all_generated).most_common(5)]
            res_txt = " | ".join([f"🎯 {x}" for x in top_picks])
            st.markdown(f"## {res_txt}")
            st.markdown("<p style='font-size:12px;'>Analisis ini ditarik langsung dari pola result 5D terakhir.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        except: st.warning("Silakan isi result 5D di Tab 1 dulu!")

    with tab4:
        st.subheader("🔄 BBFS Ultra Smart Pangkas")
        b_in = st.text_input("Masukkan Angka BBFS (Contoh: 976425):")
        col_b1, col_b2 = st.columns(2)
        with col_b1: target_pangkas = st.selectbox("Pilih Target Pangkas:", [2, 3, 4, 5], index=0)
        with col_b2: pangkas_btn = st.button(f"✂️ MULAI PANGKAS {target_pangkas}D")
        
        if pangkas_btn and b_in:
            pool_b = [c for c in b_in if c.isdigit()]
            hasil_bbfs = []
            if len(pool_b) >= target_pangkas:
                # Simulasi pangkasan 15 line terbaik
                for _ in range(10000):
                    random.shuffle(pool_b)
                    res = "".join(pool_b[:target_pangkas])
                    if res not in hasil_bbfs:
                        hasil_bbfs.append(res)
                    if len(hasil_bbfs) >= 15: break
                
                st.write(f"Berikut adalah 15 Line Terbaik dari BBFS {b_in}:")
                grid_p = '<div class="grid-container">'
                for x in hasil_bbfs:
                    grid_p += f'<div class="grid-item" style="background:#800000; border:1px solid #FFD700;">{x}</div>'
                grid_p += '</div>'
                st.markdown(grid_p, unsafe_allow_html=True)
            else:
                st.warning("Angka yang diketik kurang banyak untuk target digit tersebut!")

else: st.error("Database tidak terhubung. Cek file JSON!")
