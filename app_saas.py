import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

# CSS para el estilo Impulza
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .stButton>button { background-color: #ffc107 !important; color: #000000 !important; font-weight: 800 !important; }
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando..."):
            try:
                # La configuración más sencilla y compatible
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    # En lugar de adivinar el nombre, buscamos el archivo recién creado
                    filename = ydl.prepare_filename(info)
                
                # Transcripción directa
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Introduce una URL.")
