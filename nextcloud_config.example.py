# Plantilla de configuración de Nextcloud.
#
# Copia este archivo a "nextcloud_config.py" (ese nombre exacto) y rellena
# tus datos. "nextcloud_config.py" está en .gitignore y nunca se sube al
# repositorio: es donde van tus credenciales reales.
#
#   cp nextcloud_config.example.py nextcloud_config.py

# URL raíz de WebDAV de tu Nextcloud (termina en /remote.php/dav/)
NEXTCLOUD_URL = 'https://tu-dominio.com/remote.php/dav/'

# Tu usuario de Nextcloud (a veces es tu email, según cómo tengas
# configurado el login; pruébalo si el nombre de usuario normal no funciona)
NEXTCLOUD_USERNAME = 'tu-usuario'

# Contraseña de aplicación (NO tu contraseña normal de la cuenta).
# Se genera en: tu perfil -> Configuración -> Seguridad -> "Contraseñas de
# aplicación y dispositivos". Formato tipo xxxxx-xxxxx-xxxxx-xxxxx-xxxxx.
NEXTCLOUD_PASSWORD = 'xxxxx-xxxxx-xxxxx-xxxxx-xxxxx'

# Parejas (ID de calendario de Google, URL del calendario de Nextcloud) a
# sincronizar. Puedes añadir tantas como quieras, cada una se sincroniza
# de forma independiente.
#
# - El ID de calendario de Google: usa 'primary' para tu calendario
#   principal, o el ID de uno secundario (lo ves en Google Calendar ->
#   Configuración -> el calendario en cuestión -> "ID de calendario", con
#   forma parecida a xxxxx@group.calendar.google.com).
# - La URL del calendario de Nextcloud: la ves en el propio Nextcloud
#   (Calendario -> icono de compartir/enlace del calendario, o
#   construyéndola como
#   https://tu-dominio.com/remote.php/dav/calendars/TU_USUARIO/NOMBRE_CALENDARIO/).
CALENDAR_PAIRS = [
    ('primary', 'https://tu-dominio.com/remote.php/dav/calendars/tu-usuario/nombre-calendario/'),
    # ('otro-id-de-calendario@group.calendar.google.com',
    #  'https://tu-dominio.com/remote.php/dav/calendars/tu-usuario/otro-calendario/'),
]
