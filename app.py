import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="RIZKY V9.8 AI ASSIST", page_icon="⚔️", layout="wide")
PASSWORD_RAHASIA = "rizky77"

st.markdown("""
    <style>
    .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 5px; }
    .grid-item { background: #000; border: 1px solid #FFD700; border-radius: 4px; padding: 5px; text-align: center; color: #00FF00; font-family: monospace; font-size: 14px; font-weight: bold; }
    .slot-box { background: #001220; border: 1px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .slot-title { color: #FFD700; font-weight: bold; border-bottom: 1px solid #444; margin-bottom: 8px; font-size: 14px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 2px solid #FF4B4B; height: 3.5em; }
    .mode-invest { background:#001220; border:2px solid #00FF00; padding:15px; border-radius:10px; text-align:center; }
    .mode-bom { background:#4b0000; border:2px solid #FFD700; padding:15px; border-radius:10px; text-align:center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE & LOGIC V9.8 ---
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
        return "⚠️ SINYAL KUNING: Ada Twin Biasa. Bandar mulai main acak!", "#FFD700"
    elif max_twin >= 3:
        return "🚨 SINYAL MERAH: AWAS TWIN GILA! Bandar sedang hobi kembar 3+.", "#FF4B4B"
    return "✅ SINYAL HIJAU: Angka Bersih. Peluang JP murni tinggi.", "#00FF00"

def hitung_triangle_v9(result_str):
    try:
        n = [int(d) for d in str(result_str)]
        if len(n) >= 5:
            as_ekor = (n[0] + n[4]) % 10
            kop_kep = (n[1] + n[3]) % 10
            tengah = n[2]
            return f"{as_ekor}{kop_kep}{tengah}{as_ekor}"
        elif len(n) == 4:
            as_ekor = (n[0] + n[3]) % 10
            kop_kep = (n[1] + n[2]) % 10
            return f"{as_ekor}{kop_kep}{as_ekor}{kop_kep}"
        return "????"
    except: return "????"

db = init_conn()

if "password_correct" not in st.session_state:
    st.title("⚔️ RIZKY V9.8 AI ASSIST")
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
        with c2: a_in = st.text_input("Angka Result:", placeholder="Contoh: 16262")
        if st.button("💾 SIMPAN DATA"):
            if a_in:
                db.worksheet(f"{len(a_in)}D").append_row([str(t_in), a_in])
                st.success("Data Berhasil Disimpan!")
                st.rerun()
        st.divider()
        l_cek = st.selectbox("Cek Laci:", ["5D", "4D", "3D", "2D"])
        try:
            ws = db.worksheet(l_cek); df_hist = pd.DataFrame(ws.get_all_records())
            if not df_hist.empty:
                st.dataframe(df_hist.tail(10), use_container_width=True)
                if st.button("🗑️ HAPUS TERAKHIR"): ws.delete_rows(len(df_hist) + 1); st.rerun()
        except: st.info("Belum ada data.")

    with tab2:
        l_an = st.radio("Cek Grafik:", ["5D", "4D", "3D", "2D"], horizontal=True)
        try:
            ws_an = db.worksheet(l_an); df_an = pd.DataFrame(ws_an.get_all_records())
            if not df_an.empty:
                fig = px.area(df_an, y='Angka', title=f"Trend Gerak {l_an}"); fig.update_traces(line_color='#00FF00')
                st.plotly_chart(fig, use_container_width=True)
        except: st.warning("Input data dulu di Tab 1.")

    with tab3:
        st.subheader("🎯 Sniper AI System V9.8")
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
                
                # --- UPDATE V9.8: TWIN DETECTOR ---
                msg, color = deteksi_twin_v9(res_terakhir)
                st.markdown(f'<div style="background:{color}; color:black; padding:10px; border-radius:5px; font-weight:bold; margin-bottom:10px;">{msg}</div>', unsafe_allow_html=True)
                
                hist_str = "".join(df_an['Angka'].astype(str).tolist())
                random.seed(len(hist_str) * t_digit)
                pool = list(hist_str) + [str(j) for j in range(10)]
                random.shuffle(pool); r1 = "".join(pool[:t_digit])
                random.shuffle(pool); r2 = "".join(pool[:t_digit])
                
                angka_bom_tri = hitung_triangle_v9(res_terakhir)
                ckir, ckan = st.columns([2, 1])
                with ckir:
                    st.markdown(f'<div class="mode-invest"><h4 style="color:#00FF00; margin:0;">🛡️ INVESTASI</h4><h2 style="color:white; letter-spacing:3px;">{r1} — {r2}</h2></div>', unsafe_allow_html=True)
                with ckan:
                    st.markdown(f'<div class="mode-bom"><h4 style="color:#FFD700; margin:0;">🔥 BOM TRI</h4><h2 style="color:#FFD700; letter-spacing:3px;">{angka_bom_tri}</h2></div>', unsafe_allow_html=True)

                st.divider()
                for i in range(1, 6):
                    with st.container():
                        st.markdown(f'<div class="slot-box"><div class="slot-title">SLOT #{i}</div>', unsafe_allow_html=True)
                        snip_list = []
                        while len(snip_list) < 10:
                            random.shuffle(pool); r = "".join(pool[:t_digit])
                            if r not in snip_list: snip_list.append(r)
                        grid = '<div class="grid-container">'
                        for n in snip_list: grid += f'<div class="grid-item">{n}</div>'
                        grid += '</div></div>'
                        st.markdown(grid, unsafe_allow_html=True)
            except: st.error("Lengkapi data di Tab 1!")

    with tab4:
        st.subheader("🔄 BBFS Ultra Smart Pangkas")
        b_in = st.text_input("Ketik Angka BBFS:", key="bbfs_input")
        cb1, cb2, cb3, cb4 = st.columns(4)
        with cb1: b5 = st.button("💥 BBFS 5D"); bt=5 if b5 else None
        with cb2: b4 = st.button("💥 BBFS 4D"); bt=4 if b4 else None
        with cb3: b3 = st.button("💥 BBFS 3D"); bt=3 if b3 else None
        with cb4: b2 = st.button("💥 BBFS 2D"); bt=2 if b2 else None
        
        if (b5 or b4 or b3 or b2) and b_in:
            random.seed(len(b_in) + 77); hasil_bbfs = []
            pool_b = list(b_in)
            for _ in range(500):
                temp = pool_b.copy(); random.shuffle(temp); res = "".join(temp[:bt])
                if res not in hasil_bbfs: hasil_bbfs.append(res)
                if len(hasil_bbfs) >= 100: break
            st.session_state['current_bbfs'] = hasil_bbfs
            grid_b = '<div class="grid-container">'
            for x in hasil_bbfs: grid_b += f'<div class="grid-item">{x}</div>'
            grid_b += '</div>'; st.markdown(grid_b, unsafe_allow_html=True)

        if 'current_bbfs' in st.session_state:
            st.divider()
            if st.button("✂️ PANGKAS JADI 15 LINE (V9.8)"):
                pangkas = [line for line in st.session_state['current_bbfs'] if "2" in line or "1" in line][:15]
                st.success("15 Line Terkuat (Filter Angka Gendong 2/1)")
                grid_p = '<div class="grid-container">'
                for x in pangkas: grid_p += f'<div class="grid-item" style="background:red; border:1px solid white;">{x}</div>'
                grid_p += '</div>'; st.markdown(grid_p, unsafe_allow_html=True)

else: st.error("Database Diskonek!")
