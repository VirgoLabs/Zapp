# Temporary File Share System

A simple Django-based temporary file sharing application where users can upload files, generate shareable download links, and automatically expire/delete files after download or after a selected time period.

## Features

- Upload and share files instantly
- Generate unique download links
- One-time download support
- Automatic file expiration
- Custom expiry duration in days
- Automatic cleanup of expired files
- Simple and clean UI
- Django-based backend

---

## Tech Stack

- Python
- Django 5
- HTML/CSS
- SQLite (default Django database)

---

## Project Structure

```text
temporary file share system/
│
├── file_sharing_app/
│   ├── migrations/
│   ├── templates/
│   │   └── file_sharing_app/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── file_sharing_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd "temporary file share system"
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv env
source env/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

## How It Works

1. User uploads a file.
2. System generates a unique download link.
3. User shares the link with anyone.
4. Recipient downloads the file.
5. File is automatically deleted after download.
6. Expired files are removed automatically.

---

## Main Functionalities

### File Upload

Users can upload files directly from the home page.

### Expiry System

Files automatically expire after the selected number of days.

### One-Time Download

After a successful download:
- File is deleted from storage
- Database record is removed
- Link becomes invalid

---

## Requirements

```text
Django==5.2.14
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2026.2
```

---

## Future Improvements

- Drag and drop uploads
- File size restrictions
- Password-protected sharing
- Email sharing support
- Download analytics
- Cloud storage integration
- User authentication system

---

## License

This project is for educational and learning purposes.
