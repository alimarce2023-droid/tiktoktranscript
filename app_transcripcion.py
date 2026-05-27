import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de la página
st.set_page_config(page_title="Universal Transcript AI", page_icon="🌐")

st.title("🌐 Universal Transcript AI")
st.write("Pega el enlace de un video (TikTok, YouTube, FB, Instagram) y obtén la transcripción.")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video... Esto puede tardar según la duración."):
            try:
                # yt-dlp detecta automáticamente la plataforma por la URL
                ydl_opts = {
                    'format': 'best', 
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/120.0.0.0',
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
                st.write("Asegúrate de que el video sea público y la URL correcta.")
    else:
        st.warning("Por favor, introduce una URL válida.")
