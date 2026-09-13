import streamlit as st
import yt_dlp
import os
import tempfile

# Título y diseño de la página web
st.set_page_config(page_title="Mi Descargador de YouTube", page_icon="🎵")
st.title("🎵 Descargador de YouTube de Lau")
st.write("Pegá el link de tu video favorito para bajar el video o el MP3.")

# Cuadro de texto para pegar el enlace
url = st.text_input("🔗 Enlace de YouTube:")

# Botones de opción en la web
opcion = st.radio("¿Qué formato preferís?", ("Video (MP4)", "Solo Audio (MP3)"))

if url:
    if st.button("🚀 Preparar descarga"):
        with st.spinner("Procesando el video... Esperá un momento..."):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    
                    # Opciones para saltar las restricciones de bots en la nube
                    opciones_anti_bloqueo = {
                        'noplaylist': True,
                        'quiet': True,
                        'no_warnings': True,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['web_creator']
                            }
                        }
                    }

                    # Buscamos tu archivo cookies.txt en el repositorio de GitHub
                    if os.path.exists("cookies.txt"):
                        opciones_anti_bloqueo['cookiefile'] = 'cookies.txt'
                    else:
                        st.warning("⚠️ No se encontró el archivo 'cookies.txt'. Recordá subirlo para evitar bloqueos por bot.")

                    if opcion == "Video (MP4)":
                        ydl_opts = {
                            # Simplificado al máximo: descarga el mejor archivo único compatible con MP4 sin mezclas complejas
                            'format': 'best[ext=mp4]/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            **opciones_anti_bloqueo
                        }
                    else:
                        ydl_opts = {
                            # Simplificado al máximo: descarga el mejor audio disponible en general
                            'format': 'bestaudio/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            **opciones_anti_bloqueo
                        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        if opcion == "Solo Audio (MP3)":
                            base, _ = os.path.splitext(filename)
                            filename = base + ".mp3"

                    with open(filename, "rb") as file:
                        st.success("✨ ¡Tu archivo está listo!")
                        st.download_button(
                            label="📥 Descargar archivo en tu dispositivo",
                            data=file,
                            file_name=os.path.basename(filename),
                            mime="video/mp4" if opcion == "Video (MP4)" else "audio/mpeg"
                        )
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")
