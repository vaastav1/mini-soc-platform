# 🛡️ Mini SOC Platform

A **Security Operations Centre (SOC)** dashboard built with Python and FastAPI. Monitors Linux server authentication logs in real time, detects cyber attacks using rule-based detection, and displays live alerts on a dark-themed dashboard.

> Built as a college project to demonstrate backend development, cybersecurity concepts, and full-stack Python web development.

---

## 📸 Preview




---

## ✨ Features

- **Real-time log monitoring** — tails auth log files for new entries
- **4 detection rules** — Brute Force, Suspicious IP, Impossible Login, Privilege Escalation
- **Live dashboard** — KPI cards, events table, threat breakdown bars, timeline
- **Alert management** — acknowledge alerts, filter by type/severity, export to CSV
- **REST API** — full JSON API with auto-generated Swagger UI at `/docs`
- **Configurable** — all thresholds controlled via `.env` file
- **Attack simulator** — generate fake log entries to test detection

---

## 🔍 Detection Rules

| Rule | Trigger | Severity |
|---|---|---|
| **Brute Force** | 5+ failed SSH logins from same IP | HIGH |
| **Suspicious IP** | 10+ total events from same IP | MEDIUM |
| **Impossible Login** | Successful login after previous failures | CRITICAL |
| **Privilege Escalation** | 3+ sudo failures from same IP | HIGH |

---

## 🧰 Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Web Framework | FastAPI | Auto Swagger docs, async, type-safe |
| Database ORM | SQLAlchemy 2.0 | DB-agnostic, easy to switch to PostgreSQL |
| Database | SQLite | Zero-setup for development |
| Config | Pydantic-Settings | Type-safe `.env` loading |
| Templating | Jinja2 | Server-side rendering, built into FastAPI |
| Background Tasks | Python threading | File I/O log tailing (daemon thread) |
| Frontend | Vanilla JS + CSS | No build step, no Node.js required |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/vaastav1/mini-soc-platform.git
cd mini-soc-platform
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment file
```bash
cp .env.example .env
# Edit .env if you want to change thresholds or log path
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

### 6. Open dashboard
```
http://127.0.0.1:8000
```

Click **Run Detection** to process the sample log file and see alerts appear.

---

## 🧪 Testing with the Attack Simulator

In a second terminal (with venv activated):

```bash
# Run all attack scenarios
python simulate_attack.py all

# Or run specific scenarios
python simulate_attack.py brute_force
python simulate_attack.py impossible_login
python simulate_attack.py high_volume
```

Then click **Run Detection** on the dashboard to see the new alerts.

---

## 📁 Project Structure

```
mini-soc-platform/
│
├── app/
│   ├── main.py                  # FastAPI app, startup, dashboard route
│   ├── api/routes.py            # All /api/* REST endpoints
│   ├── core/
│   │   ├── config.py            # Settings from .env (Pydantic)
│   │   └── logging.py           # Logging setup
│   ├── db/database.py           # SQLAlchemy engine + session + init_db()
│   ├── models/security_event.py # Database table (ORM model)
│   ├── schemas/event.py         # API request/response validation (Pydantic)
│   ├── detection/
│   │   ├── engine.py            # Detection rules + in-memory counters
│   │   └── geoip.py             # IP geolocation (private vs external)
│   └── ingestor/
│       ├── log_parser.py        # Regex patterns for parsing log lines
│       ├── log_ingestor.py      # Background thread + one-shot processor
│       └── alerts.py            # Saves detected alerts to DB
│
├── logs/
│   └── sample_auth.log          # Sample Linux auth log for testing
│
├── templates/
│   └── dashboard.html           # Jinja2 dashboard template
│
├── static/style.css             # Extra CSS
├── simulate_attack.py           # Script to generate fake attack logs
├── .env.example                 # Template for environment config
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🔌 API Reference

Full interactive documentation at `http://127.0.0.1:8000/docs`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Dashboard HTML page |
| GET | `/api/events` | List all security events |
| GET | `/api/events/{id}` | Get single event |
| POST | `/api/events/{id}/ack` | Acknowledge an alert |
| GET | `/api/stats` | Summary statistics |
| POST | `/api/run-detection` | Process log file now |
| POST | `/api/reset-counters` | Reset detection counters |

---

## ⚙️ Configuration

All settings are in `.env`:

```env
BRUTE_FORCE_THRESHOLD=5       # Failed logins before brute force alert
SUSPICIOUS_IP_THRESHOLD=10    # Events from one IP before suspicious alert
ALERT_COOLDOWN_SECONDS=60     # Seconds before same alert can trigger again
LOG_FILE_PATH=logs/sample_auth.log
LOG_POLL_INTERVAL=2           # Seconds between log file checks
```

---

## 🗺️ Roadmap / Future Improvements

- [ ] User authentication (JWT tokens)
- [ ] PostgreSQL support for multi-user production deployment
- [ ] Email / Slack notifications on CRITICAL alerts
- [ ] GeoIP map visualization
- [ ] Support for more log formats (Apache, Nginx, Windows Event Log)
- [ ] Docker containerization

---

## 📚 What I Learned

- Building REST APIs with FastAPI and automatic Swagger documentation
- SQLAlchemy ORM — database models, sessions, and queries
- Real-time file monitoring using Python daemon threads
- Regular expressions for log parsing
- Cybersecurity concepts: brute force, privilege escalation, impossible travel
- Jinja2 server-side templating
- Pydantic for data validation and settings management

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Vaastav**
- GitHub: [@vaastav1](https://github.com/vaastav1)
- LinkedIn: [vaastav022626](https://www.linkedin.com/in/vaastav022626/)