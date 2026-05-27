import streamlit as st
import yt_dlp
import whisper
import os

# =========================
# CONFIG STREAMLIT
# =========================
st.set_page_config(
    page_title="Universal Transcript AI",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 Universal Transcript AI")
st.write("Pega un enlace de YouTube, TikTok, Instagram o Facebook y obtén la transcripción.")

url_video = st.text_input("URL del video:")

# =========================
# FUNCION DESCARGA AUDIO
# =========================
def descargar_audio(url):

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": "temp_audio.%(ext)s",

        # Evita logs innecesarios
        "quiet": True,
        "no_warnings": True,

        # Compatibilidad cloud
        "nocheckcertificate": True,
        "ignoreerrors": False,

        # Headers importantes
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },

        # Ayuda mucho con YouTube
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        },

        # Mejor estabilidad
        "geo_bypass": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if info is None:
            raise Exception("No se pudo obtener información del video.")

        filename = ydl.prepare_filename(info)

        return filename


# =========================
# TRANSCRIPCION
# =========================
if st.button("Transcribir ahora"):

    if not url_video:
        st.warning("Por favor introduce una URL válida.")
        st.stop()

    try:

        with st.spinner("📥 Descargando audio del video..."):

            archivo_audio = descargar_audio(url_video)

        # =========================
        # CARGA WHISPER
        # =========================
        with st.spinner("🧠 Transcribiendo con IA..."):

            model = whisper.load_model("base")

            resultado = model.transcribe(
                archivo_audio,
                fp16=False
            )

        texto = resultado["text"]

        st.success("✅ ¡Transcripción lista!")

        st.text_area(
            "Resultado:",
            texto,
            height=350
        )

        # =========================
        # BOTON DESCARGA TXT
        # =========================
        st.download_button(
            label="📄 Descargar TXT",
            data=texto,
            file_name="transcripcion.txt",
            mime="text/plain"
        )

        # =========================
        # LIMPIEZA
        # =========================
        if os.path.exists(archivo_audio):
            os.remove(archivo_audio)

    except Exception as e:

        st.error(f"❌ Error: {str(e)}")

        st.info(
            """
YouTube puede bloquear descargas desde servidores cloud como Streamlit.

Si falla solo en YouTube pero TikTok/Facebook funcionan,
el problema probablemente es bloqueo 403 de YouTube.
"""
        )
