import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

# CSS Estilo Impulza
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stTextInput label { color: #CD41C6 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; 
        border-radius: 10px !important; border: 2px solid #84139B !important;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important; color: #ffffff !important; 
        border: 2px solid #84139B !important; border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Descargando y procesando..."):
            try:
                # 1. Definimos una ruta clara y fija
                output_path = "/tmp/audio_final.mp3"
                
                # 2. Configuración forzada
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '/tmp/audio_final', # Esto evita que yt-dlp le ponga nombres raros
                    'quiet': True,
                    'no_warnings': True,
                }
                
                # 3. Descarga
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # 4. Verificación de existencia del archivo
                if os.path.exists(output_path):
                    # 5. Carga y transcripción
                    model = whisper.load_model("base")
                    resultado = model.transcribe(output_path)
                    
                    st.success("¡Transcripción lista!")
                    st.text_area("Resultado:", resultado["text"], height=300)
                    
                    # 6. Limpieza final
                    os.remove(output_path)
                else:
                    # Si llega aquí, es porque yt-dlp descargó en otro formato (ej: .webm o .m4a)
                    # Intentamos buscar cualquier archivo que empiece por audio_final
                    files = [f for f in os.listdir('/tmp/') if f.startswith('audio_final')]
                    if files:
                        model = whisper.load_model("base")
                        resultado = model.transcribe(os.path.join('/tmp/', files[0]))
                        st.success("¡Transcripción lista!")
                        st.text_area("Resultado:", resultado["text"], height=300)
                        os.remove(os.path.join('/tmp/', files[0]))
                    else:
                        st.error("Error: El archivo de audio no se generó correctamente.")
                        
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, introduce una URL válida.")
