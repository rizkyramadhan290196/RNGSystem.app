try:
    sheet = init_connection()
    all_data = sheet.get_all_values()
    
    # 1. CEK DATA SECARA AKURAT
    if len(all_data) > 1:
        # Mengambil data dan memastikan kolom sesuai dengan screenshot kamu
        df = pd.DataFrame(all_data[1:], columns=all_data[0])
        # Membersihkan spasi jika ada
        df['Angka'] = df['Angka'].astype(str).str.strip()
        df['Panjang'] = df['Angka'].apply(len)
        data_tersedia = True
    else:
        df = pd.DataFrame(columns=["Tanggal", "Jam", "Angka"])
        data_tersedia = False

    st.title("🎯 RIZKY SMART RNG V4.5")

    tab1, tab2, tab3, tab4 = st.tabs(["📥 DATABASE", "📊 ANALISIS", "🔮 PREDIKSI", "🎲 BBFS"])

    # --- TAB 1: DATABASE ---
    with tab1:
        col_in, col_hist = st.columns([1, 2])
        with col_in:
            st.subheader("Input Sesi")
            with st.form("form_v4", clear_on_submit=True):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi (Jam)")
                angka_in = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if jam and angka_in:
                        sheet.append_row([str(tgl), jam, str(angka_in)])
                        st.success("Tersimpan! Refresh halaman ya.")
                        st.rerun()
        with col_hist:
            st.subheader("Riwayat")
            if data_tersedia:
                st.table(df.tail(10)) # Menggunakan st.table agar lebih rapi di HP
            else:
                st.info("Belum ada data.")

    # --- TAB 3: PREDIKSI (SULAP AGAR MUNCUL) ---
    with tab3:
        st.subheader("🔮 Generator Prediksi")
        if data_tersedia:
            mode = st.selectbox("Pilih Target:", ["2D", "3D", "4D", "5D"])
            jml_m = st.number_input("Jumlah Urutan:", min_value=1, value=25)
            
            if st.button("MULAI RACIK"):
                # Mencari angka hot dari data yang kamu input (56478, dll)
                hot_ekor = df['Angka'].str[-1].mode()[0]
                
                hasil_final = []
                for _ in range(int(jml_m)):
                    prefix = "".join([str(random.randint(0,9)) for _ in range(int(mode[0])-1)])
                    hasil_final.append(prefix + hot_ekor)
                
                st.code(", ".join(list(set(hasil_final))))
                st.success(f"Analisis sukses berdasarkan Ekor: {hot_ekor}")
        else:
            st.warning("Silakan isi data di Tab DATABASE dulu!")

except Exception as e:
    st.error(f"Terjadi sinkronisasi: {e}")
