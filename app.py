with tab_db:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("🛰️ Input Data")
            target = st.selectbox("Pilih Pasaran:", ["TTM 5D", "TTM 4D", "KINGKONG 4D"])
            with st.form("input_form"):
                tgl = st.date_input("Tanggal", datetime.now())
                jam = st.text_input("Sesi/Jam", value=target)
                val = st.text_input("Hasil Angka")
                if st.form_submit_button("SIMPAN DATA"):
                    if val.isdigit():
                        sheet.append_row([str(tgl), jam, val])
                        st.success("Tersimpan!"); st.rerun()
            
            # --- FITUR PENGHAPUS (DI SINI PERBAIKANNYA) ---
            st.markdown("---")
            st.subheader("🗑️ Alat Pembersih")
            col_del1, col_del2 = st.columns(2)
            with col_del1:
                if st.button("Hapus Terakhir"):
                    if len(all_data) > 1:
                        sheet.delete_rows(len(all_data))
                        st.warning("Data terakhir dihapus!")
                        st.rerun()
            with col_del2:
                # Tombol hapus semua dengan konfirmasi
                if st.checkbox("Konfirmasi Reset"):
                    if st.button("HAPUS SEMUA"):
                        # Menyisakan header (baris 1)
                        sheet.resize(rows=1)
                        sheet.resize(rows=100)
                        st.error("DATABASE DIBERSIHKAN!")
                        st.rerun()
        with c2:
            st.markdown("### 📜 Log 8 Data Terakhir")
            if data_exists: 
                st.table(df.tail(8))
            else:
                st.info("Database Kosong. Silakan Input Data.")
