import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Menggunakan tanda kutip tiga agar kunci aman dari error karakter HP
KUNCI_PRIVATE = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCeQBsSgeHvBR7k
LnPf0flbUcaRQiMVf56oCmyvg0QUAI3SvPzQK3UuVaOdF3PmXK6X10JRyiWCSA/m
ZCkZ9lrsqvebWoER7Rg4QMkUDtnkzIPQTOfxY5Wf/iWn4XfMOB6QNy2vPxJJz8B7
tz5AEZVme4JLMKMFG2PdsxUIDnJ1DXSVvb6dczn8f+4+lLvZYWoLnMHqyVLPwbls
r7JdOGY5Q6qAjArb72xFSayRxKXLgBJKxsV6rOiwDNdkJz/JB2amenb04dyN7VKX
EH/sOvu6Rtr+MWIYd6jbZ3kHeSwMxtESfd27/OADaCSbRZX6shfTii6zaeHZme+E
C2s6S4G/AgMBAAECggEAHHiuJjtF+eny79zHrjop4dspnZLHmyOV2OffPAii4/Jh
nkcu8tHtNHuP7htTkXkrIgrsQzIRREUqDydC1cF1ZaIEuAT5cQGxm0iAdzUUKwNZm
1MAxbsWa8ukXv0eadRyXqxyyVHhFgxAksl16jq5bMdAA1iRPACk4Y3fHzeZDg3l6
qJeZpkdYlR7ZMlYd2jRgTpHNzRye9AeE4O3MUH+ES3+gDBtsRQt7vilPOb7T7LYA
CblT4PhA5vCLshzspEZfNqTzJSC4zu0D7ScBJMKjDPCxqyCcIPzn3W/ZFYCONuXu
SaKSSnP5gFxG1rOfNxsqKWn5puf/tTViLp33dmwGAQKBgQDX6Gcou4x43sA8Krr9
i2wpsAa2Mb44tZf3C5Gf2WTPVdN18YNjd8NYNvJaDjDAWFwYlPWBkMaYBIa93icI
oiSjGICzSf11WI/AQ9rXU90gNPj9kTYqYNZa41PqEzKmBhZLGxVobqwe2GXbJP9C
R4nogXgT2KbhB9epHcAoZdoUvwKBgQC7otiRG8jGGYcFk2ueYbXi3owdl9vr6GPi
BmRphzIJ7+yUGFOzx0TKZY4R/HzeGX7X6VSxh0iE1qehUH2EhvsBR6ubiwXL+qPK
Kc6stCl+WCDM6Ds3rr/Vhy7Wo0ysjdyuL33pJ2bFX2zdQKMqwgVlsf0yAGUyQHxE
yv0TiKjTAQKBgQCOKxgSeDytMm/+rlxmq7HTWXdx7RtGmDyyjcmcKjf5VphhZ2CO
1MOqiLPYnNN5NDWgciWe5Uf/vatDxs6JHstlIbNNW4EsDd7KSWQGudA3buotfbre
+NjtDBerYGzPad6wIetc0tM/lFqtjJUQfa7PjMEWwGhScSmO0GpBr5+EXQKBgCLd
xcRhF1PIVpCwriTGH1hC5mJxX4pcqoLLkUkSuDekf5+dTaBwfNXnPRkWg9V5g1p3
ydF7jHQ+WE+ZbSEqIu6V6cVlEQtFNZyIldxOuyhT6cD2E0mibsR3aBAw/Skf8dW
R91VVwGCE+ahJjDB0OLuyg/KhwNpfC4EUjaZBFYBAoGALYrSRObhiUC+TYbjkle1
UtR+djS1JXt/TVcQKMBHq9Qee2+dd5sJ/a1I0F1sO91jUOrZog/U0V71xJeagqJn
O4zRgszw/5dzPnoMUkraebnknW03ptyT3qXfGnE8W2qjyjvWSJTBmvFd1zSKupNj
b8kIxnLA92W3zIgxyiVDq9c=
-----END PRIVATE KEY-----"""

INFO_KREDENSIAL = {
  "type": "service_account",
  "project_id": "rng-database-486403",
  "private_key_id": "1313e482fc6df0927a5254b2c068372829cd3cce",
  "private_key": KUNCI_PRIVATE,
  "client_email": "database-rizky@rng-database-486403.iam.gserviceaccount.com",
  "client_id": "118379763658129966317",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/database-rizky%40rng-database-486403.iam.gserviceaccount.com"
}

def connect_to_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(INFO_KREDENSIAL, scopes=scope)
    return gspread.authorize(creds).open("Database_RNG_Rizky").get_worksheet(0)

st.title("🎯 DATABASE RIZKY V3")

try:
    sheet = connect_to_sheet()
    st.success("✅ BERHASIL TERHUBUNG!")
    with st.form("input", clear_on_submit=True):
        tgl = st.date_input("Tanggal", datetime.now())
        jam = st.text_input("Sesi Jam")
        angka = st.text_input("Angka")
        if st.form_submit_button("SIMPAN DATA"):
            sheet.append_row([str(tgl), jam, angka])
            st.success(f"Angka {angka} Berhasil Disimpan!")
except Exception as e:
    st.error(f"Gagal: {e}")
