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
                    
                    # Opciones preparadas para funcionar en la nube (Streamlit Cloud)
                    opciones_anti_bloqueo = {
                        'noplaylist': True,
                        'quiet': True,
                        'no_warnings': True,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['ios'],
                                'formats': ['missing_pot']
                            }
                        }
                    }

                    # Buscamos el archivo cookies.txt que subiste a GitHub
                    if os.path.exists("cookies.txt"):
                        opciones_anti_bloqueo['cookiefile'] = 'cookies.txt'
                    else:
                        st.warning("⚠️ No se encontró el archivo 'cookies.txt'. El script intentará descargar sin credenciales, pero podría fallar.")

                    if opcion == "Video (MP4)":
                        ydl_opts = {
                            # Corregido: Si falla el protocolo m3u8_native, salta automáticamente al mejor MP4 clásico disponible
                            'format': 'bv[protocol=m3u8_native]+ba[protocol=m3u8_native]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            **opciones_anti_bloqueo
                        }
                    else:
                        ydl_opts = {
                            # Corregido: Busca el mejor audio disponible en cualquier protocolo compatible
                            'format': 'ba[protocol=m3u8_native]/bestaudio/best',
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
