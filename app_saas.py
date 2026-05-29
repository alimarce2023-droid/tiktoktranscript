import streamlit as st
import yt_dlp
import whisper
import os
import openai # IMPORTANTE: Necesitas esta librería para que la IA escriba el guion

# Configuración
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")

st.title("ProTranscribe - Impulza Digital")

# Aquí configurarías tu API KEY en los Secrets de Streamlit
# st.secrets["OPENAI_API_KEY"]

def generar_guion_ia(texto, plataforma):
    # Esto es lo que "reescribe" de verdad el texto
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = f"Eres un experto en redes sociales. Reescribe este guion para {plataforma} enfocándote en SEO y viralidad, creando un gancho, cuerpo y llamado a la acción: {texto}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ... (El resto de tu lógica de transcripción igual) ...

# En el paso 2, donde antes hacíamos el "corte y pega", ahora llamamos a la IA:
if st.button("Generar Nuevo Guion IA"):
    with st.spinner("La IA está escribiendo tu guion..."):
        nuevo_guion = generar_guion_ia(st.session_state.transcripcion, plataforma)
        st.text_area("Resultado profesional:", nuevo_guion, height=300)
