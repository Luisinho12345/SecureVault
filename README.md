@'
# SecureVault

A professional desktop password manager built with Python, featuring AES encryption, a PIN-protected vault, and a modern dark-themed interface.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-2563EB)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Secure Authentication** — account registration and login with bcrypt password hashing
- **Encrypted Vault** — all stored passwords are encrypted with Fernet (AES) before being saved to the database
- **PIN Protection** — a separate 4-6 digit PIN is required to view or copy any password, even within an authenticated session
- **Password Generator** — customizable length and character sets, with real-time strength feedback
- **Dashboard** — overview of total, strong and weak passwords, categories, and visual charts
- **Search & Categories** — instant search and category-based organization
- **Backups** — create and restore full database backups from within the app
- **Activity Logging** — all key actions (login attempts, password changes) are logged to file
- **Toast Notifications** — non-intrusive feedback for every action
- **Splash Screen** — branded loading screen on startup

## Screenshots

*(add your screenshots here, e.g. `docs/screenshot-dashboard.png`)*

## Technologies

- **Python 3.14**
- **CustomTkinter** — modern UI framework built on Tkinter
- **SQLite** — local database
- **cryptography (Fernet)** — password encryption
- **bcrypt** — password/PIN hashing
- **Pillow** — icon rendering
- **Matplotlib** — dashboard charts

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/YOUR_USERNAME/SecureVault.git
   cd SecureVault
```

2. Create and activate a virtual environment:
```bash
   python -m venv .venv
   .venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Run the application:
```bash
   python main.py
```

## Project Structure