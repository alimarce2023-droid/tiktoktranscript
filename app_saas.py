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
        with st.spinner("Descargando y procesando..."):
            try:
                # Ruta segura en /tmp para la nube
                output_path = "/tmp/audio_final.mp3"
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                    'outtmpl': '/tmp/audio_final',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                model = whisper.load_model("base")
                resultado = model.transcribe(output_path)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists(output_path):
                    os.remove(output_path)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, introduce una URL válida.")
