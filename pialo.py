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
    # Creamos un botón web para iniciar el proceso
    if st.button("🚀 Preparar descarga"):
        with st.spinner("Procesando el video... Esperá un momento..."):
            try:
                # Usamos una carpeta temporal del servidor para procesar el archivo
                with tempfile.TemporaryDirectory() as tmpdir:
                    
                    if opcion == "Video (MP4)":
                        ydl_opts = {
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'noplaylist': True, # Esto evita que baje listas enteras por error
                        }
                    else:
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'noplaylist': True,
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        # Si elegimos MP3, yt-dlp cambia la extensión al final del proceso
                        if opcion == "Solo Audio (MP3)":
                            filename = os.path.splitext(filename)[0] + ".mp3"

                    # Leemos el archivo descargado para dárselo al usuario
                    with open(filename, "rb") as file:
                        st.success("✨ ¡Tu archivo está listo!")
                        # Crea el botón web oficial para guardar el archivo en la PC/Celular del usuario
                        st.download_button(
                            label="📥 Descargar archivo en tu dispositivo",
                            data=file,
                            file_name=os.path.basename(filename),
                            mime="video/mp4" if opcion == "Video (MP4)" else "audio/mpeg"
                        )
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")
