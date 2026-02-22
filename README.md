# 💬 ChatApp — Real-Time Chat with Django Channels

A full-featured real-time chat application built with **Django Channels**, **WebSockets**, and **WebRTC**. Features an iMessage-inspired dark mode UI with support for media sharing, voice notes, audio calling, and more.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 💬 Messaging
- Real-time text messaging via WebSockets
- Emoji picker (7 categories, 200+ emoji)
- Reply / quote messages with inline preview
- Message search with highlight & navigation
- Typing indicator ("User is typing…" with animated dots)
- Smart scroll — only auto-scrolls when you're at the bottom
- "New messages" floating button when scrolled up

### 📎 Media & Files
- Image, video, and file attachments
- Camera capture (take photos directly)
- Voice note recording with timer
- Drag & drop file upload
- Image preview lightbox
- File download

### 📞 Calling
- WebRTC audio calling (peer-to-peer)
- Incoming call popup with ringtone
- Mute / speaker controls
- Call timer
- Minimize / restore call UI

### 🔔 Notifications & Presence
- Online user presence tracking
- Browser push notifications (when tab is hidden)
- Toast notifications for events

### ⚡ Technical
- WebSocket reconnection with exponential backoff (no page reload)
- Keyboard shortcuts (Escape closes modals)
- PWA support (installable, offline caching)
- Admin dashboard for user management

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5, Django Channels, Daphne (ASGI) |
| Database | PostgreSQL |
| Cache/Broker | Redis (Channel Layer) |
| Frontend | HTML, CSS (Tailwind), Vanilla JavaScript |
| Real-time | WebSockets, WebRTC |
| Deployment | Docker, Docker Compose, Ngrok |

---

## 🚀 Quick Start (Docker)

### Prerequisites

Make sure you have these installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Git](https://git-scm.com/downloads)

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/chat.git
cd chat
```

### Step 2: Create the environment file

Create a `.env` file in the project root (or edit the existing one):

```env
# Django
DJANGO_SECRET=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# PostgreSQL
POSTGRES_DB=chatdb
POSTGRES_USER=chatuser
POSTGRES_PASSWORD=chatpass

# Ngrok (optional — for public URL access)
NGROK_AUTHTOKEN=your-ngrok-token
```

> **Tip:** For local development, the default values work fine. Change `DJANGO_SECRET` to any random string for security.

### Step 3: Build and run

```bash
docker compose up --build
```

This will:
1. Build the Django application image
2. Start PostgreSQL, Redis, and the web server
3. Run database migrations automatically
4. Create a default admin user
5. Start the Daphne ASGI server

### Step 4: Open the app

Open your browser and go to:

```
http://localhost:8000
```

### Step 5: Log in

Default credentials:

| Username | Password |
|----------|----------|
| `admin`  | `admin`  |

> ⚠️ **Change the default password** in production! Go to the admin dashboard at `/admin/` to manage users.

---

## 💡 How to Use

### Start Chatting

1. Log in at `http://localhost:8000`
2. Navigate to a chat room: `http://localhost:8000/chat/general/`
3. Type a message and hit Send (or press Enter)

### Multi-User Testing

To test real-time features (typing indicator, calls, etc.):

1. Open a **second browser tab** (or use incognito mode)
2. Log in as a different user
3. Go to the same chat room
4. Start chatting — you'll see messages, typing indicators, and presence updates in real-time

### Create New Users

1. Log in as `admin`
2. Go to `http://localhost:8000/dashboard/`
3. Fill in the "Create User" form
4. The new user can now log in

### Join a Chat Room

Chat rooms are created automatically. Just navigate to any room URL:

```
http://localhost:8000/chat/general/
http://localhost:8000/chat/team/
http://localhost:8000/chat/random/
```

Replace `general`, `team`, or `random` with any room name you like.

---

## 📁 Project Structure

```
chat/
├── chatapp/                  # Main Django app
│   ├── consumers.py          # WebSocket handlers
│   ├── models.py             # Database models
│   ├── views.py              # HTTP views
│   ├── views_media.py        # Media upload endpoint
│   ├── views_call_recording.py  # Call recording endpoint
│   ├── routing.py            # WebSocket URL routing
│   ├── urls.py               # HTTP URL routing
│   ├── admin.py              # Django admin config
│   └── templates/
│       ├── chat_room.html    # Main chat interface
│       ├── login.html        # Login page
│       └── admin_create_user.html  # Admin dashboard
├── chatproject/              # Django project config
│   ├── settings.py           # Settings
│   ├── urls.py               # Root URL config
│   └── asgi.py               # ASGI config (WebSocket + HTTP)
├── static/
│   ├── sw.js                 # Service Worker (PWA)
│   └── manifest.json         # PWA manifest
├── docker-compose.yml        # Docker services
├── Dockerfile                # App container
├── entrypoint.sh             # Container startup script
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

---

## 🔧 Common Commands

```bash
# Start all services
docker compose up --build

# Start in background
docker compose up --build -d

# Stop all services
docker compose down

# View logs
docker compose logs -f web

# Open a Django shell
docker compose exec web python manage.py shell

# Create a superuser manually
docker compose exec web python manage.py createsuperuser

# Run migrations manually
docker compose exec web python manage.py migrate
```

---

## 🌐 Public Access with Ngrok

The project includes Ngrok for exposing your local server to the internet:

1. Sign up at [ngrok.com](https://ngrok.com) and get your auth token
2. Add it to `.env`: `NGROK_AUTHTOKEN=your-token`
3. Restart: `docker compose up --build`
4. Check the Ngrok container logs for your public URL:
   ```bash
   docker compose logs ngrok
   ```

---

## 🧪 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port 8000 already in use** | Stop other services on port 8000, or change the port in `docker-compose.yml` |
| **Database connection error** | Wait a few seconds — PostgreSQL may still be starting. Check with `docker compose logs db` |
| **WebSocket won't connect** | Make sure you're using `http://localhost:8000`, not `127.0.0.1` (must match `ALLOWED_HOSTS`) |
| **Can't access microphone/camera** | Use HTTPS (Ngrok) or `localhost` — browsers block media APIs on plain HTTP |
| **Docker build fails** | Run `docker compose down -v` to clean volumes, then rebuild |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
