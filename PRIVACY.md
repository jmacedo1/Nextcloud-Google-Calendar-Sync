# Política de privacidad

Este proyecto (`Nextcloud-Google-Calendar-Sync`) es un script de uso personal
que sincroniza los eventos de tu propio calendario de Google Calendar con tu
propio calendario de Nextcloud.

- El script se ejecuta localmente (o en un servidor propio, como un
  Raspberry Pi / DietPi) bajo el control exclusivo de quien lo instala.
- Los datos de calendario (títulos de eventos, fechas y horas) se leen y
  escriben únicamente entre tu cuenta de Google y tu propia instancia de
  Nextcloud, usando tus propias credenciales.
- Ningún dato se envía, comparte ni almacena en ningún servidor de terceros
  ni por los autores de este proyecto. No hay recogida de datos, analítica
  ni telemetría de ningún tipo.
- Las credenciales (token de Google, usuario/contraseña de Nextcloud)
  quedan únicamente en los archivos locales de configuración de quien
  ejecuta el script (`token.json`, `credentials.json`,
  `nextcloud_config.py`), y nunca se suben al repositorio.

Al ser software de código abierto para uso personal, cada persona que lo
instala es responsable de sus propios datos y credenciales.
