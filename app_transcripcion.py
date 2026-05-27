import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de la página
st.set_page_config(page_title="Universal Transcript AI", page_icon="🌐")

st.title("🌐 Universal Transcript AI")
st.write("Pega el enlace de un video y obtén la transcripción.")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video... Esto puede tardar según la duración."):
            try:
                # Configuramos yt-dlp para imitar un navegador real y evitar el 403
                # NOTA: Si el error 403 persiste, TikTok requiere autenticación vía cookies.
                ydl_opts = {
                    'format': 'best', 
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'nocheckcertificate': True,
                    # Forzamos cabeceras adicionales para parecer una petición legítima de navegador
                    'http_headers': {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Sec-Fetch-Mode': 'navigate',
                    }
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
                st.write("Si el error 403 persiste, TikTok ha bloqueado la IP de Streamlit. Intenta con un video de YouTube para comprobar que la app funciona correctamente.")
    else:
        st.warning("Por favor, introduce una URL válida.")
