# AI Meeting Task Manager

## Project Overview

AI Meeting Task Manager is a small full-stack application that helps convert unstructured meeting notes into actionable tasks.

Users can paste meeting notes into the application and the system will use an AI model to extract structured tasks automatically.
These tasks can then be managed through a simple dashboard where users can update status, assign time, and track completion.

Typical workflow:

1. Paste meeting notes into the extraction panel
2. The backend AI service converts text into task objects
3. Tasks are stored in the database
4. The dashboard displays tasks sorted by time
5. Users can update status or delete tasks

---

## Features

* Extract tasks automatically from meeting notes using AI
* Create tasks manually
* Assign optional time to tasks
* View tasks sorted by time
* Mark tasks as completed
* Delete tasks
* Filter tasks (All / Pending / Completed)

---

## Tech Stack

**Frontend**

* React
* Vite

**Backend**

* Flask REST API

**Database**

* SQLite (Relational Database)

**AI Extraction**

* LLM-based task extraction service

---

## Architecture

```
React Frontend
      │
      ▼
Flask REST API
      │
      ▼
Task Service Layer
      │
      ▼
SQLite Database
      │
      ▼
AI Extraction Service
```

The frontend communicates with the backend using REST APIs.
The backend handles business logic, AI task extraction, and data persistence.

---

## Key Technical Decisions

### Flask for Backend
Flask was chosen because it is lightweight and suitable for building REST APIs quickly. The project uses Flask blueprints and a service layer to keep routing logic separate from business logic.

### React + Vite for Frontend
React was used to create a responsive task dashboard. Vite provides fast development builds and hot module reloading, improving development speed.

### SQLite Database
SQLite was selected for simplicity and because it requires no external setup. It is sufficient for a small task management system.

### AI Task Extraction
A language model is used to convert unstructured meeting notes into structured tasks. The system attempts to extract tasks and optional time references from text.

### Time-based Task Ordering
Tasks are stored with an optional scheduled_time field and displayed in time order to make the dashboard easier to scan.

---

## Project Structure

```
ai-meeting-task-manager
│
├── backend
│   ├── routes
│   │   └── tasks.py
│   ├── services
│   │   ├── task_service.py
│   │   └── ai_service.py
│   ├── tests
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── services
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── screenshots
│   ├── dashboard.png
│   └── extraction.png
│
├── README.md
└── .gitignore
```

* backend = Flask API and business logic
* frontend = React user interface
* services = AI extraction and task logic
* routes = REST API endpoints
* screenshots = UI examples for documentation

---

## API Endpoints

| Method | Endpoint             | Description                       |
| ------ | -------------------- | --------------------------------- |
| GET    | `/tasks`             | Retrieve all tasks sorted by time |
| POST   | `/tasks`             | Create a new task                 |
| PATCH  | `/tasks/{id}/status` | Update task status                |
| DELETE | `/tasks/{id}`        | Delete a task                     |
| POST   | `/tasks/extract`     | Extract tasks from meeting notes  |
| GET    | `/health`            | Backend health check              |

---

## Installation

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m flask --app app run
```

Backend runs at:

```
http://127.0.0.1:5000
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## Screenshots



### Dashboard

![Dashboard](screenshots/dashboard.png)

### Task Extraction

![Task Extraction](screenshots/extraction.png)

### Task List (Scheduled Times)

![Task List](screenshots/task-list.png)

---

## AI Task Extraction

The system uses a language model to convert meeting notes into structured tasks.

Example input:

```
Prepare slides for tomorrow
Finish backend implementation
Schedule client meeting
```

Example extracted tasks:

```
Prepare slides
Finish backend implementation
Schedule client meeting
```

If a task does not contain time information, the backend assigns a default time slot so tasks remain ordered.

---

## Future Improvements

* User authentication
* Role-based task assignment
* Email notifications for pending tasks
* Calendar integration
* Task priority levels
