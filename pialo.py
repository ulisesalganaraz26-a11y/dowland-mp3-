import streamlit as st
import requests

# Configuración de diseño adaptada para pantallas de celulares
st.set_page_config(page_title="Mi Descargador de Música", page_icon="🎵", layout="centered")
st.title("🎵 Descargador de Música de Lau")
st.write("Descargá tus videos o MP3 directo al celular sin bloqueos.")

# Cuadro de texto para pegar el enlace
url = st.text_input("🔗 Enlace de YouTube:")

# Botones de opción en la web
opcion = st.radio("¿Qué formato preferís?", ("Solo Audio (MP3)", "Video (MP4)"))

def descargar_con_cobalt(video_url, modo):
    # CORREGIDO: Se agregó '/api/json' que es la ruta correcta que pide Cobalt para procesar
    api_url = "https://cobalt.tools"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Configuramos los parámetros necesarios
    payload = {
        "url": video_url,
        "videoQuality": "720",
        "audioFormat": "mp3",
        "isAudioOnly": True if modo == "Solo Audio (MP3)" else False,
        "downloadMode": "audio" if modo == "Solo Audio (MP3)" else "default"
    }
    
    try:
        respuesta = requests.post(api_url, json=payload, headers=headers)
        
        # Si la API responde bien, procesamos el JSON
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos.get("status") in ["stream", "redirect"]:
                return datos.get("url"), None
            elif datos.get("status") == "picker":
                return datos.get("picker").get("url"), None
            elif datos.get("status") == "error":
                # Si Cobalt nos da un error interno (ej. video muy largo), lo mostramos
                return None, datos.get("error", {}).get("code", "Error desconocido en Cobalt")
            
            return None, f"El servidor respondió con un estado desconocido: {datos.get('status')}"
        else:
            return None, f"El servidor de descargas está ocupado (Error {respuesta.status_code})."
            
    except Exception as e:
        return None, f"Error de conexión en la nube: {e}"

if url:
    # Botón adaptado para celulares
    if st.button("🚀 Preparar descarga", use_container_width=True):
        with st.spinner("Procesando archivo... Esperá un momento..."):
            download_url, error = descargar_con_cobalt(url, opcion)
            
            if error:
                st.error(f"❌ {error}")
            elif download_url:
                st.success("✨ ¡Tu archivo está listo!")
                # Botón llamativo para tocar desde el celular
                st.markdown(
                    f'<a href="{download_url}" target="_blank" style="display: block; width: 100%; text-align: center; padding: 0.75em; color: white; background-color: #28a745; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin-top: 10px;">📥 DESCARGAR EN MI CELULAR</a>',
                    unsafe_allow_html=True
                )
