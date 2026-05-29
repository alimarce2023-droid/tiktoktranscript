import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #ffffff !important; text-transform: uppercase; }
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #ffc107 !important; 
        color: #000000 !important; 
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 15px !important;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #5a189a !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")
st.write("Pega el enlace de un video y obtén la transcripción.")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando... Esto puede tomar un minuto."):
            try:
                # Opciones más robustas
                ydl_opts = {
                    'format': 'bestaudio',
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    filename = ydl.prepare_filename(info)
                
                # Carga y transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Si el error persiste, es posible que el sitio bloquee al servidor. Intenta con un video diferente.")
    else:
        st.warning("Por favor, introduce una URL válida.")
