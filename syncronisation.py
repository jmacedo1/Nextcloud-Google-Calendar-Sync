import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from caldav import DAVClient, Calendar
from icalendar import Calendar as ICalCalendar
from nextcloud_config import NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, CALENDAR_PAIRS

# Permisos (scopes) para la API de Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Ruta al archivo de credenciales para la API de Google
CREDENTIALS_FILE = './credentials.json'

# Ventana de sincronización: desde hoy hasta este número de días adelante
SYNC_DAYS = 30

# Conexión a la API de Google Calendar
def connect_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    from googleapiclient.discovery import build
    service = build('calendar', 'v3', credentials=creds)
    return service

# Conexión al servidor de Nextcloud vía CalDAV (compartida para todos los calendarios)
def connect_nextcloud_client():
    return DAVClient(
        url=NEXTCLOUD_URL,
        username=NEXTCLOUD_USERNAME,
        password=NEXTCLOUD_PASSWORD
    )

# Obtener los eventos de un calendario de Google Calendar
def get_google_events(service, google_calendar_id='primary'):
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + datetime.timedelta(days=SYNC_DAYS)).isoformat() + 'Z'
    events_result = service.events().list(calendarId=google_calendar_id, timeMin=time_min,
                                          timeMax=time_max,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    google_events = []
    
    for event in events:
        event_summary = event.get('summary', 'Sin título')

        # Comprobar si el evento dura todo el día o varios días
        if 'dateTime' in event['start']:
            start = event['start']['dateTime']
            end = event['end']['dateTime']
        else:
            start = event['start']['date']
            end = event['end']['date']

        google_events.append({
            'summary': event_summary,
            'start': start,
            'end': end
        })
    
    return google_events

# Obtener los eventos de Nextcloud
def get_nextcloud_events(calendar):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=SYNC_DAYS)
    events = calendar.date_search(start=start, end=end, expand=True)
    return events

# Extraer el SUMMARY real de un evento de Nextcloud, sin verse afectado
# por el plegado de líneas largas del formato iCal (RFC 5545)
def _nc_event_summary(nc_event):
    ical = ICalCalendar.from_ical(nc_event.data)
    for component in ical.walk('VEVENT'):
        return str(component.get('summary', ''))
    return ''

# Sincronizar los eventos de Google hacia Nextcloud
def sync_google_to_nextcloud(google_events, nextcloud_calendar):
    for event in google_events:
        event_summary = event['summary']
        start = event['start']
        end = event['end']

        # Convertir las fechas al formato datetime
        if "T" in start:
            start_dt = datetime.datetime.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            end_dt = datetime.datetime.strptime(end[:19], "%Y-%m-%dT%H:%M:%S")
        else:
            start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end, "%Y-%m-%d")

        # Comprobar si el evento ya existe en Nextcloud
        nc_events = get_nextcloud_events(nextcloud_calendar)
        event_exists = any(_nc_event_summary(nc_event) == event_summary for nc_event in nc_events)

        if not event_exists:
            # Añadir el evento a Nextcloud con el formato correcto
            if "T" in start:
                ical_event = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Product//EN
BEGIN:VEVENT
SUMMARY:{event_summary}
DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}
END:VEVENT
END:VCALENDAR"""
            else:
                ical_event = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Product//EN
BEGIN:VEVENT
SUMMARY:{event_summary}
DTSTART;VALUE=DATE:{start_dt.strftime('%Y%m%d')}
DTEND;VALUE=DATE:{end_dt.strftime('%Y%m%d')}
END:VEVENT
END:VCALENDAR"""

            nextcloud_calendar.save_event(ical_event)
            print(f"Añadido a Nextcloud: {event_summary}")

# Sincronizar los eventos de Nextcloud hacia Google
def sync_nextcloud_to_google(service, nextcloud_calendar, google_calendar_id='primary'):
    nc_events = get_nextcloud_events(nextcloud_calendar)
    google_events = get_google_events(service, google_calendar_id)
    existing_summaries = {g_event['summary'] for g_event in google_events}

    for nc_event in nc_events:
        ical = ICalCalendar.from_ical(nc_event.data)
        vevent = next(iter(ical.walk('VEVENT')), None)
        if vevent is None:
            continue

        event_summary = str(vevent.get('summary', 'Sin título'))
        dtstart = vevent['dtstart'].dt
        dtend_prop = vevent.get('dtend')
        is_all_day = not isinstance(dtstart, datetime.datetime)

        if is_all_day:
            dtend = dtend_prop.dt if dtend_prop else dtstart + datetime.timedelta(days=1)
        else:
            dtend = dtend_prop.dt if dtend_prop else dtstart + datetime.timedelta(hours=1)
            # Normalizar a UTC los eventos con hora (vengan en UTC o con TZID)
            if dtstart.tzinfo:
                dtstart = dtstart.astimezone(datetime.timezone.utc)
            if dtend.tzinfo:
                dtend = dtend.astimezone(datetime.timezone.utc)

        # Comprobar si el evento ya existe en Google Calendar
        if event_summary in existing_summaries:
            continue

        if is_all_day:
            event = {
                'summary': event_summary,
                'start': {'date': dtstart.strftime('%Y-%m-%d')},
                'end': {'date': dtend.strftime('%Y-%m-%d')},
            }
        else:
            event = {
                'summary': event_summary,
                'start': {
                    'dateTime': dtstart.strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': dtend.strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
                    'timeZone': 'UTC',
                },
            }

        service.events().insert(calendarId=google_calendar_id, body=event).execute()
        existing_summaries.add(event_summary)
        print(f"Añadido a Google: {event_summary}")

def main():
    # Conexión a Google Calendar
    google_service = connect_google_calendar()

    # Conexión al servidor de Nextcloud (compartida para todos los calendarios)
    nextcloud_client = connect_nextcloud_client()

    # Sincronizar cada pareja (calendario de Google, calendario de Nextcloud)
    for google_calendar_id, nextcloud_calendar_url in CALENDAR_PAIRS:
        print(f"--- Sincronizando {google_calendar_id} <-> {nextcloud_calendar_url} ---")
        nextcloud_calendar = Calendar(client=nextcloud_client, url=nextcloud_calendar_url)

        # Sincronizar Google hacia Nextcloud
        google_events = get_google_events(google_service, google_calendar_id)
        sync_google_to_nextcloud(google_events, nextcloud_calendar)

        # Sincronizar Nextcloud hacia Google
        sync_nextcloud_to_google(google_service, nextcloud_calendar, google_calendar_id)

if __name__ == '__main__':
    main()
