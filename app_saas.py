import streamlit as st
import yt_dlp
import whisper
import os

# Configuración visual Impulza Digital
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; font-weight: 800; }
    .stButton>button { background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

# Sesión para guardar la transcripción
if 'transcripcion' not in st.session_state:
    st.session_state.transcripcion = None

url_video = st.text_input("URL del video:")

# PASO 1: Transcripción
if st.button("Paso 1: Transcribir Video"):
    if url_video:
        with st.spinner("Descargando y transcribiendo..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '/tmp/temp_audio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                resultado = whisper.load_model("base").transcribe("/tmp/temp_audio.mp3")
                st.session_state.transcripcion = resultado["text"]
                st.success("¡Transcripción obtenida con éxito!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Introduce una URL.")

# PASO 2: Guion SEO (Solo aparece si ya hay una transcripción)
if st.session_state.transcripcion:
    st.divider()
    st.subheader("Paso 2: Generar Guion SEO")
    plataforma = st.selectbox("Selecciona la plataforma:", ["TikTok", "Instagram", "YouTube Shorts", "LinkedIn"])
    
    if st.button("Generar Guion Optimizado"):
        texto = st.session_state.transcripcion
        st.markdown(f"### Estrategia para {plataforma}")
        
        # Lógica de ejemplo según plataforma
        if plataforma == "TikTok":
            estructura = f"Gancho: ¡Deja de hacer esto si quieres crecer!\n\nContenido: {texto[:400]}...\n\nCTA: Sígueme para más."
            tags = "#ImpulzaDigital #Viral #IA"
        else:
            estructura = f"Título: Aprende hoy sobre esto.\n\nContenido: {texto[:400]}...\n\nConclusión: Visita el link."
            tags = "#ImpulzaDigital #Marketing #Estrategia"
            
        st.text_area("Resultado:", estructura, height=250)
        st.markdown(f"**Hashtags:** {tags}")
