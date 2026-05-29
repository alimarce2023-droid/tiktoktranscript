import streamlit as st
import yt_dlp
import whisper
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración inicial de la página
st.set_page_config(page_title="ProTranscribe SaaS", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    /* Botones con fondo morado y letra negra */
    .stButton>button { 
        background-color: #84139B !important; 
        color: #000000 !important; 
        font-weight: bold !important;
        border: none !important;
    }
    .stTextInput>div>div>input { background-color: #1A1A1A; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe SaaS")

# 1. LÓGICA DE GOOGLE SHEETS
def guardar_lead(email):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
    # Usamos los secrets de Streamlit configurados en la nube
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    sheet = client.open("Leads_ProTranscribe").sheet1
    sheet.append_row([email])

# 2. INTERFAZ (Ya no requiere login)
tab1, tab2 = st.tabs(["Nueva Transcripción", "Captar Leads"])

with tab1:
    url = st.text_input("URL del video:")
    if st.button("Transcribir"):
        if url:
            st.write("Procesando video...")
        else:
            st.warning("Por favor, pega una URL.")
        
with tab2:
    email = st.text_input("Correo del cliente:")
    if st.button("Guardar en Sheets"):
        try:
            guardar_lead(email)
            st.success("Correo guardado con éxito en la hoja de cálculo.")
        except Exception as e:
            st.error(f"Error al conectar con Google Sheets: {e}")
