# Nextcloud-Google-Calendar-Sync

Este proyecto permite sincronizar automáticamente los eventos entre un calendario de Nextcloud y una cuenta de Google Calendar. Utiliza la API de Nextcloud y la API de Google Calendar para facilitar la gestión de tus eventos en ambas plataformas. Ideal para mantener al día tus citas y eventos en varios calendarios de forma transparente.

Para conseguir el `credentials.json` necesitas crear un proyecto en Google Cloud Console y generar unas credenciales OAuth de tipo "aplicación de escritorio". Pasos:

1. Ve a **https://console.cloud.google.com/** e inicia sesión con la cuenta de Google cuyo calendario quieres sincronizar.
2. Arriba a la izquierda, crea un **proyecto nuevo** (o selecciona uno existente) — botón "Seleccionar proyecto" → "Proyecto nuevo".
3. En el menú lateral: **APIs y servicios → Biblioteca**, busca **"Google Calendar API"** y pulsa **Habilitar**.
4. Ve a **APIs y servicios → Pantalla de consentimiento OAuth**:
   - Tipo de usuario: **Externo** (a menos que tengas Google Workspace).
   - Rellena nombre de la app, tu email, etc.
   - En "Usuarios de prueba" añade tu propia cuenta de Gmail (mientras la app no esté publicada, solo esas cuentas podrán autenticarse).
5. Ve a **APIs y servicios → Credenciales → Crear credenciales → ID de cliente de OAuth**:
   - Tipo de aplicación: **Aplicación de escritorio**.
   - Ponle un nombre (ej. "nextcloud-sync") y crea.
6. Te aparecerá un botón para **descargar el JSON** — descárgalo, renómbralo a `credentials.json` y colócalo en la misma carpeta que `syncronisation.py`.

<img width="706" alt="image" src="https://github.com/user-attachments/assets/46851e10-f1c2-484f-9f1b-31d21a950a19">
<img width="394" alt="image" src="https://github.com/user-attachments/assets/603c1f75-f391-45dd-bd85-fed490cbf3b8"> 
<img width="539" alt="image" src="https://github.com/user-attachments/assets/8311c1fe-440c-42de-a15d-6ed04530951d"> 
<img width="548" alt="image" src="https://github.com/user-attachments/assets/7d43a0b8-c8da-40fc-8c84-a4f205d32a4f"> 
<img width="549" alt="image" src="https://github.com/user-attachments/assets/4418453c-5971-4e24-a122-40d16486111d"> 
<img width="489" alt="image" src="https://github.com/user-attachments/assets/e0ec9fbc-3957-4c99-8673-445d16107763"> 
<img width="451" alt="image" src="https://github.com/user-attachments/assets/0462ea60-1c66-475a-9119-44e2aa503ab5">

Durante la primera ejecución, se te pedirá que inicies sesión con la cuenta de Google que quieres sincronizar (esto creará un archivo token que te reconectará automáticamente en cada ejecución posterior). Inicia sesión y tu calendario se sincronizará ¡en ambos sentidos!

(Después puedes configurarlo como una tarea cron en un servidor Linux, pero eso queda fuera del alcance de este tutorial.)

---

Fork en castellano de [enfantme/Nextcloud-Google-Calendar-Sync](https://github.com/enfantme/Nextcloud-Google-Calendar-Sync).

## Licencia

Este fork se distribuye bajo licencia [MIT](LICENSE).
