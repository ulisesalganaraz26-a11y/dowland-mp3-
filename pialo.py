# Buscamos el archivo cookies.txt que subiste a GitHub
if os.path.exists("cookies.txt"):
    opciones_anti_bloqueo['cookiefile'] = 'cookies.txt'
else:
    st.warning("⚠️ No se encontró el archivo 'cookies.txt'. El script intentará descargar sin credenciales, pero podría fallar.")
