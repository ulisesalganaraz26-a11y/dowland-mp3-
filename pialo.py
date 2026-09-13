import streamlit as st
import requests
import re

# Configuración de diseño adaptada para pantallas de celulares
st.set_page_config(page_title="Mi Descargador de Música", page_icon="🎵", layout="centered")
st.title("🎵 Descargador de Música de Lau")
st.write("Pegá el link de YouTube para descargar tu MP3 o Video directo a tu celular.")

# Cuadro de texto para pegar el enlace
url = st.text_input("🔗 Enlace de YouTube:")

# Botones de opción en la web
opcion = st.radio("¿Qué formato preferís?", ("Solo Audio (MP3)", "Video (MP4)"))

def obtener_descarga_api(video_url, modo):
    # Extraer el ID del video de YouTube mediante expresiones regulares
    video_id_match = re.search(r'(?:v=|\/v\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})', video_url)
    if not video_id_match:
        return None, "Enlace de YouTube no válido o mal copiado."
    
    video_id = video_id_match.group(1)
    
    # Usamos un servidor espejo (API pública y2mate) que salta los bloqueos de la nube
    url_analizar = "https://y2mate.com"
    payload_analizar = {
        'k_query': f'https://youtube.com{video_id}',
        'k_page': 'home',
        'hl': 'en',
        'q_auto': 0
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }
    
    try:
        res1 = requests.post(url_analizar, data=payload_analizar, headers=headers).json()
        if res1.get('status') != 'success':
            return None, "YouTube bloqueó la petición temporalmente. Intentá con otro video."
        
        v_id = res1.get('v_id')
        links = res1.get('links', {})
        selected_key = None
        
        # Filtrado de formatos sin requerir yt-dlp local
        if modo == "Solo Audio (MP3)":
            mp3_options = links.get('mp3', {})
            if mp3_options:
                selected_key = list(mp3_options.values())[0].get('k')
        else:
            mp4_options = links.get('mp4', {})
            if mp4_options:
                selected_key = list(mp4_options.values())[0].get('k')
                
        if not selected_key:
            for cat in links.values():
                for opt in cat.values():
                    if (modo == "Solo Audio (MP3)" and opt.get('f') == 'mp3') or (modo == "Video (MP4)" and opt.get('f') == 'mp4'):
                        selected_key = opt.get('k')
                        break
        
        if not selected_key:
            return None, "Formato no disponible para este video en específico."
            
        # Petición final para empaquetar el enlace de descarga directo
        url_convertir = "https://y2mate.com"
        payload_convertir = {
            'type': 'youtube',
            '_id': v_id,
            'v_id': video_id,
            'ajax': '1',
            'token': '',
            'ftype': 'mp3' if modo == "Solo Audio (MP3)" else 'mp4',
            'fquality': '128' if modo == "Solo Audio (MP3)" else '720',
            'k': selected_key
        }
        
        res2 = requests.post(url_convertir, data=payload_convertir, headers=headers).json()
        if res2.get('status') != 'success':
            return None, "Error del servidor al procesar el archivo."
            
        html_resultado = res2.get('result', '')
        link_final_match = re.search(r'href="([^"]+)"', html_resultado)
        
        if link_final_match:
            return link_final_match.group(1), None
        else:
            return None, "No se pudo generar el enlace de descarga."
            
    except Exception as e:
        return None, f"Error en el servidor de la nube: {e}"

if url:
    # Botón grande adaptado para pantallas táctiles de celulares
    if st.button("🚀 Preparar descarga", use_container_width=True):
        with st.spinner("Procesando... Esperá un momento..."):
            download_url, error = obtener_descarga_api(url, opcion)
            
            if error:
                st.error(f"❌ {error}")
            elif download_url:
                st.success("✨ ¡Tu archivo está listo!")
                # Botón de descarga con estilo llamativo para el celular
                st.markdown(
                    f'<a href="{download_url}" target="_blank" style="display: block; width: 100%; text-align: center; padding: 0.75em; color: white; background-color: #28a745; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin-top: 10px;">📥 DESCARGAR EN MI CELULAR</a>',
                    unsafe_allow_html=True
                )
