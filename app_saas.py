import streamlit as st
import yt_dlp
import whisper
import os

st.set_page_config(page_title="ProTranscribe Pro", layout="wide")

st.title("ProTranscribe - Impulza Digital")

# Opción 1: URL
url = st.text_input("URL del video (Si falla, usa la subida de abajo):")

# Opción 2: Subida manual (El plan infalible)
archivo = st.file_uploader("O sube el video/audio desde tu PC:", type=['mp4', 'mp3', 'wav'])

if st.button("Transcribir"):
    # Elegimos el archivo (URL o Subido)
    archivo_a_procesar = None
    
    if archivo:
        archivo_a_procesar = "temp_local.mp3"
        with open(archivo_a_procesar, "wb") as f:
            f.write(archivo.getbuffer())
    elif url:
        with st.spinner("Intentando descargar de la URL..."):
            try:
                ydl_opts = {'format': 'bestaudio', 'outtmpl': '/tmp/audio_final'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                if os.path.exists('/tmp/audio_final.mp3'):
                    archivo_a_procesar = '/tmp/audio_final.mp3'
                else:
                    st.error("No se pudo descargar. Por favor, descarga el video en tu PC y súbelo aquí.")
            except Exception as e:
                st.error(f"Error de descarga: {e}")

    # Procesar
    if archivo_a_procesar:
        with st.spinner("Transcribiendo..."):
            model = whisper.load_model("base")
            res = model.transcribe(archivo_a_procesar)
            st.text_area("Resultado:", res["text"], height=300)
            if os.path.exists(archivo_a_procesar):
                os.remove(archivo_a_procesar)
