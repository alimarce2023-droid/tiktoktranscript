import streamlit as st
import yt_dlp
import whisper
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="centered")

# Estilos CSS con estética Impulza Digital
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; font-family: sans-serif; }
    
    /* Contenedor del Login/Landing */
    .login-box {
        background-color: #161616;
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #5a189a;
        text-align: center;
        margin-top: 50px;
    }
    
    /* Botón Amarillo estilo Impulza */
    .stButton>button { 
        background-color: #ffc107 !important; 
        color: #000000 !important; 
        font-weight: bold !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        padding: 15px !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #242424 !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Lógica de Sesión
if 'acceso_concedido' not in st.session_state:
    st.session_state.acceso_concedido = False

# 1. LÓGICA DE GOOGLE SHEETS
def guardar_lead(nombre, email):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads_ProTranscribe").sheet1
    sheet.append_row([nombre, email])

# 2. PÁGINA DE INICIO (LOGIN)
if not st.session_state.acceso_concedido:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("IMPULZA DIGITAL")
    st.subheader("VERIFICACIÓN DE ACCESO")
    st.write("Ingresa tus datos para comprobar si tienes una invitación pendiente o unirte a la lista VIP.")
    
    nombre = st.text_input("", placeholder="Nombre Completo")
    email = st.text_input("", placeholder="Correo Electrónico")
    
    if st.button("Continuar →"):
        if nombre and email:
            guardar_lead(nombre, email)
            st.session_state.acceso_concedido = True
            st.rerun()
        else:
            st.warning("Por favor completa ambos campos.")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. INTERFAZ PRINCIPAL (Solo visible tras registro)
else:
    st.title("ProTranscribe por Impulza Digital")
    
    tab1, tab2 = st.tabs(["🚀 Transcripción", "📩 Más Info"])
    
    with tab1:
        url_video = st.text_input("", placeholder="Pega aquí la URL del video...")
        if st.button("Transcribir ahora"):
            if url_video:
                with st.spinner("Procesando contenido..."):
                    try:
                        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp_audio.%(ext)s', 'quiet': True}
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url_video, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        model = whisper.load_model("base")
                        resultado = model.transcribe(filename)
                        
                        st.success("¡Transcripción generada!")
                        st.text_area("Resultado final:", resultado["text"], height=300)
                        if os.path.exists(filename): os.remove(filename)
                    except Exception as e:
                        st.error(f"Error procesando: {e}")
            else:
                st.warning("Por favor, introduce una URL válida.")
