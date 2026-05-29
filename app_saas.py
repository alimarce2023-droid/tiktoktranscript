import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página con tus colores de marca
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stTextInput label { color: #CD41C6 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: 800 !important; 
        border-radius: 10px !important;
        border: 2px solid #84139B !important;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important; 
        color: #ffffff !important; 
        border: 2px solid #84139B !important; 
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")
st.write("Pega el enlace de un video y obtén la transcripción.")

url_video = st.text_input("URL del video:")

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
                st.write("Si el error persiste, el sitio puede haber bloqueado la conexión del servidor.")
    else:
        st.warning("Por favor, introduce una URL válida.")
