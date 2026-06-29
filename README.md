# Ticket Reservation API — TravelBus Events

**Studente:** Nya Emmanuel
**Matricola:** 7146768
**Corso:**PPM 2026

## Tipo di progetto

**REST API**

## Framework utilizzato

**Django REST Framework (DRF)**, basato su Django 6.0.

## Descrizione

Ticket Reservation API è un back-end REST per la gestione di eventi e
delle relative prenotazioni di posti. Gli utenti anonimi possono
consultare gli eventi disponibili; gli utenti registrati (Attendee)
possono prenotare, modificare e annullare le proprie prenotazioni;
gli organizzatori (Organizer) possono creare, modificare ed eliminare
i propri eventi e consultare l'elenco degli iscritti.

L'autenticazione è basata su **Token Authentication** (Django REST
Framework `authtoken`). Il sistema implementa permessi basati sul
ruolo dell'utente, validazione dei dati in ingresso tramite serializer
e gestione automatica della disponibilità dei posti.

## Funzionalità implementate (per ruolo)

### Utente anonimo
- Consultare la lista degli eventi disponibili (`GET /api/events/`).
- Consultare il dettaglio di un evento (`GET /api/events/{id}/`).

### Attendee (utente standard registrato)
- Registrarsi e ottenere un token di autenticazione.
- Visualizzare il proprio profilo (`/api/auth/me/`).
- Creare una prenotazione per un evento, con controllo automatico
  della disponibilità dei posti.
- Visualizzare, modificare e annullare **solo le proprie**
  prenotazioni.

### Organizer (organizzatore di eventi)
- Creare, modificare ed eliminare **i propri** eventi.
- Visualizzare l'elenco degli iscritti (`attendees`) ai propri eventi.
- Non può modificare eventi creati da altri organizer.

## Modelli e relazioni

- `accounts.User` (modello utente personalizzato, estende
  `AbstractUser`, con campo `role`: `ATTENDEE` o `ORGANIZER`).
- `events.Event` — `ForeignKey` verso `User` (campo `organizer`).
- `reservations.Reservation` — `ForeignKey` verso `User` (campo
  `user`) e `ForeignKey` verso `Event` (campo `event`).

Sono quindi presenti **3 relazioni** tra tabelle (Event→User,
Reservation→User, Reservation→Event), superiori al minimo richiesto.

## Struttura del progetto

```
ticket_reservation_api/
├── manage.py
├── requirements.txt
├── Procfile
├── README.md
├── db.sqlite3                  ← database demo pre-popolato
├── ticketapi/                  ← configurazione progetto Django
│   ├── settings.py
│   └── urls.py
├── accounts/                   ← app: utenti e autenticazione
│   ├── models.py                  (modello User personalizzato)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── events/                      ← app: gestione eventi
│   ├── models.py                  (modello Event)
│   ├── serializers.py
│   ├── permissions.py             (IsOrganizerOrReadOnly)
│   ├── views.py                   (EventViewSet, azione attendees)
│   ├── urls.py
│   └── management/commands/seed_demo_data.py
└── reservations/                ← app: gestione prenotazioni
    ├── models.py                  (modello Reservation)
    ├── serializers.py
    ├── permissions.py             (IsOwner)
    ├── views.py                   (ReservationViewSet, azione cancel)
    └── urls.py
```

## Installazione locale

```bash
# 1. Clona il repository
git clone <URL_DEL_REPOSITORY>
cd ticket_reservation_api

# 2. Crea e attiva un ambiente virtuale
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Applica le migrazioni
#    
python manage.py migrate

# 5. Ripopola i dati demo da zero
python manage.py seed_demo_data

# 6. Avvia il server di sviluppo
python manage.py runserver
```

L'API sarà disponibile su `http://127.0.0.1:8000/`.

## Database demo

Il file **`db.sqlite3`** incluso nel repository contiene già:
- 3 account demo (vedi sotto).
- 4 eventi di esempio.
- 3 prenotazioni di esempio (2 confermate, 1 annullata).

## Account demo

| Username        | Password       | Ruolo                          |
|-----------------|----------------|---------------------------------|
| `admin_demo`    | `admin12345`   | Superuser + Organizer (accesso anche a `/admin/`) |
| `manager_demo`  | `manager12345` | Organizer (organizzatore eventi) |
| `user_demo`     | `user12345`    | Attendee (utente standard)       |

## Link di deployment

> **Da completare dopo il deploy:**
> `https://NOME-PROGETTO.onrender.com`

### Come effettuare il deploy su Render (gratuito)

1. Crea un account su [render.com](https://render.com) e collega il
   repository GitHub.
2. Crea un nuovo **Web Service**, selezionando il repository.
3. Imposta:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn ticketapi.wsgi:application`
4. Aggiungi le variabili d'ambiente:
   - `SECRET_KEY` → una stringa segreta a piacere
   - `DEBUG` → `False`
   - `ALLOWED_HOSTS` → `*` (o il domino fornito da Render)
5. Esegui il deploy e copia l'URL fornito da Render nel campo sopra.

## Documentazione degli endpoint

| Metodo | URL                              | Autenticazione | Ruolo richiesto      | Body (esempio)                                   | Risposta (esempio)                                          | Descrizione |
|--------|-----------------------------------|-----------------|------------------------|---------------------------------------------------|--------------------------------------------------------------|-------------|
| POST   | `/api/auth/register/`            | No              | —                      | `{"username":"mario","email":"m@x.com","password":"pass123"}` | `{"user": {...}, "token": "..."}`                            | Registra un nuovo utente (ruolo default ATTENDEE) e restituisce il token. |
| POST   | `/api/auth/login/`                | No              | —                      | `{"username":"user_demo","password":"user12345"}` | `{"token": "abcd1234..."}`                                   | Effettua il login e restituisce il token da usare nelle richieste successive. |
| GET    | `/api/auth/me/`                   | Sì (Token)      | Qualsiasi utente loggato | —                                                  | `{"id":3,"username":"user_demo","role":"ATTENDEE",...}`      | Restituisce il profilo dell'utente autenticato. |
| GET    | `/api/events/`                    | No              | Pubblico               | —                                                  | `{"count":4,"results":[{...}]}`                               | Lista paginata di tutti gli eventi disponibili. |
| GET    | `/api/events/{id}/`               | No              | Pubblico               | —                                                  | `{"id":1,"title":"Concerto Jazz al Parco",...}`               | Dettaglio di un evento specifico. |
| POST   | `/api/events/`                    | Sì (Token)      | ORGANIZER              | `{"title":"Workshop","location":"Firenze","date":"2026-12-01T18:00:00Z","seats_total":30}` | `{"id":5,"title":"Workshop",...}`                             | Crea un nuovo evento (l'organizer viene impostato automaticamente). |
| PUT/PATCH | `/api/events/{id}/`            | Sì (Token)      | ORGANIZER proprietario | `{"seats_total":40}`                              | `{"id":5,"seats_total":40,...}`                               | Aggiorna un evento (solo se sei l'organizer che lo ha creato). |
| DELETE | `/api/events/{id}/`               | Sì (Token)      | ORGANIZER proprietario | —                                                  | `204 No Content`                                              | Elimina un evento (solo organizer proprietario). |
| GET    | `/api/events/{id}/attendees/`     | Sì (Token)      | ORGANIZER proprietario | —                                                  | `[{"id":1,"username":"user_demo","seats_booked":5,...}]`      | Elenco delle prenotazioni confermate per l'evento (azione specifica per ruolo). |
| GET    | `/api/reservations/`              | Sì (Token)      | Utente autenticato     | —                                                  | `{"count":3,"results":[{...}]}`                               | Lista delle **proprie** prenotazioni. |
| POST   | `/api/reservations/`              | Sì (Token)      | Utente autenticato     | `{"event":1,"seats_booked":2}`                    | `{"id":4,"event":1,"seats_booked":2,"status":"CONFIRMED",...}` | Crea una prenotazione (valida la disponibilità dei posti). |
| GET    | `/api/reservations/{id}/`         | Sì (Token)      | Proprietario           | —                                                  | `{"id":1,"event_title":"Concerto Jazz al Parco",...}`         | Dettaglio di una propria prenotazione. |
| PATCH  | `/api/reservations/{id}/`         | Sì (Token)      | Proprietario           | `{"seats_booked":3}`                              | `{"id":1,"seats_booked":3,...}`                               | Aggiorna una propria prenotazione. |
| DELETE | `/api/reservations/{id}/`         | Sì (Token)      | Proprietario           | —                                                  | `204 No Content`                                              | Elimina una propria prenotazione. |
| POST   | `/api/reservations/{id}/cancel/`  | Sì (Token)      | Proprietario           | —                                                  | `{"id":1,"status":"CANCELLED",...}`                           | Annulla una prenotazione e libera i posti sull'evento. |

Tutte le risposte di errore (validazione, permessi negati,
autenticazione mancante) restituiscono JSON con codice di stato HTTP
appropriato (`400`, `401`, `403`, `404`).

## Testing con HTTPie

Il progetto utilizza **[HTTPie](https://httpie.io/)** come client di
test minimo, come previsto dalle linee guida del corso.

### Installazione di HTTPie

```bash
pip install httpie
```

### URL di base

```bash
# Locale
BASE=http://127.0.0.1:8000

# Online (dopo il deploy)
BASE=https://NOME-PROGETTO.onrender.com
```

### 1. Login e recupero del token

```bash
http POST $BASE/api/auth/login/ username=user_demo password=user12345
```

Risposta:
```json
{
    "token": "43ae1e9fcd162fbfff7a12ab8416b72498312010"
}
```

Salva il token in una variabile per le richieste successive:

```bash
TOKEN=43ae1e9fcd162fbfff7a12ab8416b72498312010
```

### 2. Chiamata a un endpoint pubblico (senza autenticazione)

```bash
http GET $BASE/api/events/
```

### 3. Chiamata a un endpoint autenticato

```bash
http GET $BASE/api/auth/me/ "Authorization:Token $TOKEN"
```

### 4. Creare una prenotazione (Attendee)

```bash
http POST $BASE/api/reservations/ "Authorization:Token $TOKEN" \
    event=1 seats_booked=2
```

### 5. Annullare una prenotazione

```bash
http POST $BASE/api/reservations/1/cancel/ "Authorization:Token $TOKEN"
```

### 6. Login come Organizer e creare un evento

```bash
http POST $BASE/api/auth/login/ username=manager_demo password=manager12345
ORG_TOKEN=<token_ricevuto>

http POST $BASE/api/events/ "Authorization:Token $ORG_TOKEN" \
    title="Workshop di Fotografia" \
    location="Firenze" \
    date="2026-12-01T18:00:00Z" \
    seats_total=30
```

### 7. Test di un'azione vietata (permessi)

Un Attendee che tenta di creare un evento deve ricevere `403 Forbidden`:

```bash
http POST $BASE/api/events/ "Authorization:Token $TOKEN" \
    title="Tentativo non autorizzato" location="Firenze" \
    date="2026-12-01T18:00:00Z" seats_total=10
```

Risposta attesa:
```json
{
    "detail": "Non hai l'autorizzazione per eseguire questa azione."
}
```

### 8. Organizer consulta gli iscritti al proprio evento

```bash
http GET $BASE/api/events/1/attendees/ "Authorization:Token $ORG_TOKEN"
```

## Pannello di amministrazione Django

È disponibile anche il pannello admin standard di Django su `/admin/`,
accessibile con l'account `admin_demo` / `admin12345`, utile per
ispezionare rapidamente i dati durante la valutazione.
