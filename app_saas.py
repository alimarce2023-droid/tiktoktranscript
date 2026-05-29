import streamlit as st
import yt_dlp
import whisper
import os
import time

st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

st.title("ProTranscribe por Impulza Digital")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Descargando y procesando..."):
            try:
                # Usamos /tmp, el único lugar donde Streamlit tiene permisos totales de escritura
                output_path = "/tmp/audio_final.mp3"
                
                # Configuramos yt-dlp para guardar en /tmp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                    'outtmpl': '/tmp/audio_final',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # Verificar existencia en /tmp
                if not os.path.exists(output_path):
                    raise Exception("yt-dlp no pudo crear el archivo en /tmp")
                
                # Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(output_path)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza
                if os.path.exists(output_path):
                    os.remove(output_path)
                    
            except Exception as e:
                st.error(f"Error crítico: {e}")
    else:
        st.warning("Introduce una URL.")
