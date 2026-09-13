# Nextcloud-Google-Calendar-Sync

Este proyecto permite sincronizar automáticamente los eventos entre un calendario de Nextcloud y una cuenta de Google Calendar. Utiliza la API de Nextcloud y la API de Google Calendar para facilitar la gestión de tus eventos en ambas plataformas. Ideal para mantener al día tus citas y eventos en varios calendarios de forma transparente.

Para conseguir el `credentials.json` necesitas crear un proyecto en Google Cloud Console y generar unas credenciales OAuth de tipo "aplicación de escritorio". Pasos:

1. Ve a **https://console.cloud.google.com/** e inicia sesión con la cuenta de Google cuyo calendario quieres sincronizar.
2. Crea un proyecto nuevo (o selecciona uno existente): arriba a la izquierda, en el selector de proyecto, pulsa **"Proyecto nuevo"**, ponle un nombre (ej. `nextcloud`) y créalo.
3. Habilita la API: en el menú lateral ve a **APIs y servicios → Biblioteca**, busca **"Google Calendar API"** y pulsa **Habilitar**. Comprueba que queda en estado "Habilitada".
4. Configura la pantalla de consentimiento (en la consola actual aparece como **"Google Auth Platform"**):
   - En el menú lateral, entra en **"Público"** (Audience).
   - Tipo de usuario: **Externo** (a menos que tengas Google Workspace, en cuyo caso puedes usar "Interno").
   - Rellena los datos obligatorios: nombre de la app, email de asistencia, email de contacto de desarrollador. Guarda.
   - En esa misma pantalla, mientras el estado de publicación sea **"Testing"**, busca la sección **"Usuarios de prueba"** y pulsa **"+ Add users"**. Añade ahí la cuenta de Gmail/Google cuyo calendario vas a sincronizar — solo las cuentas añadidas aquí podrán iniciar sesión con la app mientras no la publiques.
5. Crea el cliente OAuth: en el menú lateral ve a **"Clientes"** (o pulsa el botón **"Crear cliente de OAuth"** que aparece en "Descripción general").
   - **Tipo de aplicación: "Aplicación de escritorio"** — es importante no elegir "Aplicación web", porque el script abre un servidor local para el login (`flow.run_local_server`).
   - Nombre: algo identificable, ej. `nextcloud-sync`.
   - Pulsa **Crear**.
6. Descarga las credenciales: en la lista de **"Clientes"**, abre el que acabas de crear y descarga el JSON (icono de descarga). Renómbralo a `credentials.json` y colócalo en la misma carpeta que `syncronisation.py`.

<img width="706" alt="image" src="https://github.com/user-attachments/assets/46851e10-f1c2-484f-9f1b-31d21a950a19">
<img width="394" alt="image" src="https://github.com/user-attachments/assets/603c1f75-f391-45dd-bd85-fed490cbf3b8"> 
<img width="539" alt="image" src="https://github.com/user-attachments/assets/8311c1fe-440c-42de-a15d-6ed04530951d"> 
<img width="548" alt="image" src="https://github.com/user-attachments/assets/7d43a0b8-c8da-40fc-8c84-a4f205d32a4f"> 
<img width="549" alt="image" src="https://github.com/user-attachments/assets/4418453c-5971-4e24-a122-40d16486111d"> 
<img width="489" alt="image" src="https://github.com/user-attachments/assets/e0ec9fbc-3957-4c99-8673-445d16107763"> 
<img width="451" alt="image" src="https://github.com/user-attachments/assets/0462ea60-1c66-475a-9119-44e2aa503ab5">

## Instalar dependencias

En Debian/Ubuntu recientes, `pip` no deja instalar paquetes a nivel de sistema (PEP 668), así que usa un entorno virtual dentro del proyecto. Si tu sistema no tiene ya `venv`/`pip` de Python (por ejemplo, en imágenes mínimas como DietPi), instálalos primero:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
```

Y luego crea el entorno e instala las dependencias:

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-auth-oauthlib google-api-python-client caldav icalendar
```

Cada vez que abras una terminal nueva para ejecutar el script, reactiva el entorno con `source venv/bin/activate` (o selecciona el intérprete `venv/bin/python` en VS Code).

## Configurar Nextcloud y los calendarios a sincronizar

Copia la plantilla [`nextcloud_config.example.py`](nextcloud_config.example.py) a `nextcloud_config.py` (ese nombre exacto) y rellena tus datos — este segundo archivo está en `.gitignore` y nunca se sube al repositorio, es donde van tus credenciales reales:

```bash
cp nextcloud_config.example.py nextcloud_config.py
```

Dentro de `nextcloud_config.py` tienes que indicar:

- **`NEXTCLOUD_URL`**: la URL raíz de WebDAV de tu Nextcloud (termina en `/remote.php/dav/`).
- **`NEXTCLOUD_USERNAME`** y **`NEXTCLOUD_PASSWORD`**: tu usuario de Nextcloud y una contraseña de aplicación (Configuración → Seguridad → "Contraseñas de aplicación y dispositivos" — nunca tu contraseña normal).
- **`CALENDAR_PAIRS`**: la lista de parejas que quieres sincronizar, cada una con el **ID del calendario de Google** (`'primary'` para el principal, o el ID de uno secundario) y la **URL del calendario de Nextcloud** correspondiente. Puedes añadir tantas parejas como quieras — cada una se sincroniza de forma independiente.

Durante la primera ejecución, se te pedirá que inicies sesión con la cuenta de Google que quieres sincronizar (esto creará un archivo token que te reconectará automáticamente en cada ejecución posterior). Inicia sesión y tu calendario se sincronizará ¡en ambos sentidos!

(Después puedes configurarlo como una tarea cron en un servidor Linux, pero eso queda fuera del alcance de este tutorial.)

---

Fork en castellano de [enfantme/Nextcloud-Google-Calendar-Sync](https://github.com/enfantme/Nextcloud-Google-Calendar-Sync).

## Licencia

Este fork se distribuye bajo licencia [MIT](LICENSE).
