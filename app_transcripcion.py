mport streamlit as st
import yt_dlp
import whisper
import os

# Configuración de la página
st.set_page_config(page_title="ProTranscribe AI", layout="wide")

# Estilos CSS con tus colores de marca
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stSidebar { background-color: #4D184A; }
    .stButton>button { background-color: #84139B; color: #FFFFFF; border-radius: 10px; font-weight: bold; }
    .stTextInput>div>div>input { border: 2px solid #CD41C6; background-color: #1A1A1A; color: white; }
    h1, h2, h3 { color: #FFCC00; }
    </style>
""", unsafe_allow_html=True)

# Menú de navegación
menu = st.sidebar.radio("Navegación", ["Dashboard", "Nueva Transcripción", "Mi Cuenta"])

if menu == "Dashboard":
    st.title("Hola de nuevo 👋")
    st.write("Bienvenido a tu panel de control.")
    st.info("Aquí aparecerá tu historial de transcripciones próximamente.")

elif menu == "Nueva Transcripción":
    st.title("🎙️ Nueva Transcripción")
    url = st.text_input("Pega aquí la URL del video (TikTok, YouTube, FB, IG):")
    
    if st.button("Transcribir ahora"):
        if url:
            with st.spinner("Procesando con IA..."):
                try:
                    # Lógica de descarga
                    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp_audio.%(ext)s', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                    
                    # Lógica de transcripción
                    model = whisper.load_model("base")
                    res = model.transcribe(filename)
                    
                    st.success("¡Transcripción completa!")
                    st.text_area("Resultado:", res["text"], height=300)
                    
                    if os.path.exists(filename): os.remove(filename)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Ingresa una URL válida.")

elif menu == "Mi Cuenta":
    st.title("Configuración")
    st.write("Tu plan actual: **Gratuito**")
