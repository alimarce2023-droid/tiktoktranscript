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

# 2. INTERFAZ
tab1, tab2 = st.tabs(["Nueva Transcripción", "Captar Leads"])

with tab1:
    url_video = st.text_input("URL del video (YouTube, TikTok, etc.):")
    if st.button("Transcribir ahora"):
        if url_video:
            with st.spinner("Procesando video... Esto puede tardar según la duración."):
                try:
                    # Configuramos yt-dlp con la lógica que te funcionaba
                    ydl_opts = {
                        'format': 'bestaudio/best', 
                        'outtmpl': 'temp_audio.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'nocheckcertificate': True,
                        'ignoreerrors': False,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_video, download=True)
                        filename = ydl.prepare_filename(info)
                    
                    # Carga del modelo Whisper
                    model = whisper.load_model("base")
                    resultado = model.transcribe(filename)
                    
                    st.success("¡Transcripción lista!")
                    st.text_area("Resultado:", resultado["text"], height=300)
                    
                    # Limpieza
                    if os.path.exists(filename):
                        os.remove(filename)
                        
                except Exception as e:
                    st.error(f"Error procesando el video: {e}")
                    st.write("Tip: YouTube/TikTok puede bloquear el acceso a servidores de la nube. Si el error persiste, asegúrate de que el video no tenga restricciones.")
        else:
            st.warning("Por favor, introduce una URL válida.")
        
with tab2:
    email = st.text_input("Correo del cliente:")
    if st.button("Guardar en Sheets"):
        try:
            guardar_lead(email)
            st.success("Correo guardado con éxito en la hoja de cálculo.")
        except Exception as e:
            st.error(f"Error al conectar con Google Sheets: {e}")
