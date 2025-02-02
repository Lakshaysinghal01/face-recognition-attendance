# Face Recognition Attendance System

A robust attendance management system using facial recognition technology. Built with Flask and OpenCV, this system provides a secure and efficient way to track attendance using facial recognition.

## Features

- 👤 Face Recognition-based attendance tracking
- 📸 Multiple attendance capture methods:
  - Webcam capture
  - Photo upload
- 🔐 Secure user authentication
- 📊 Real-time attendance status
- 📈 Attendance history and statistics
- 👨‍💼 User dashboard
- 🕒 Automatic status tracking (Present/Late)

## Technology Stack

- **Backend Framework**: Flask
- **Database**: PostgreSQL
- **Face Recognition**: OpenCV with Haar Cascade
- **Frontend**: Bootstrap 5, Feather Icons
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Form Handling**: Flask-WTF
- **API Security**: PyJWT

## Prerequisites

Before running this project, make sure you have:

1. Python 3.11 or higher
2. PostgreSQL database
3. Webcam (for live capture)
4. Required Python packages (installed automatically):
   - flask
   - flask-sqlalchemy
   - flask-login
   - flask-wtf
   - opencv-python-headless
   - numpy
   - psycopg2-binary
   - werkzeug
   - email-validator
   - pyjwt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd face-recognition-attendance
```

2. Set up environment variables:
```bash
# Required environment variables
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost:5432/attendance_db
```

3. Create and initialize the database:
```bash
# The tables will be automatically created when you run the application
python main.py
```

## Project Structure

```
├── app.py              # Flask app initialization
├── auth.py             # Authentication functions
├── face_utils.py       # Face recognition utilities
├── forms.py            # Form definitions
├── models.py           # Database models
├── routes.py           # Route handlers
├── static/            
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/          # HTML templates
└── uploads/           # Uploaded images directory
```

## Usage Guide

### Registration
1. Navigate to the registration page
2. Fill in your details (username, email, password)
3. Upload a clear front-facing photo for face recognition
4. Submit the form

### Marking Attendance
1. Login to your account
2. Go to "Mark Attendance"
3. Choose either:
   - Use webcam to capture your face
   - Upload a photo manually
4. The system will verify your face and mark attendance
5. Attendance status (Present/Late) is automatically determined based on time

### Viewing Attendance
1. Check your dashboard for attendance statistics
2. View detailed attendance history
3. See current day's attendance status

## Database Schema

### Users Table
- id: Primary Key
- username: Unique username
- email: User's email
- password_hash: Hashed password
- face_encoding: Stored face recognition data
- is_admin: Admin status
- created_at: Account creation timestamp

### Attendance Table
- id: Primary Key
- user_id: Foreign Key (Users)
- timestamp: Attendance time
- status: Present/Late/Absent

## API Endpoints

### Authentication Endpoints
- POST `/login`: User login
- POST `/register`: User registration
- GET `/logout`: User logout

### Attendance Endpoints
- POST `/api/mark-attendance`: Mark attendance with face photo
- GET `/api/attendance-status`: Get current day's attendance status

### View Endpoints
- GET `/`: Home page
- GET `/dashboard`: User dashboard
- GET `/attendance`: Mark attendance page
- GET `/view_history`: View attendance history
- GET `/reports`: Access attendance reports (admin only)

## Security Features

- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Secure file upload handling
- Face recognition verification
- Session management
- JWT-based API authentication

## Running the Application

1. Start the server:
```bash
python main.py
```

2. Access the application at:
```
http://localhost:5000
```

## Development

The application runs in debug mode by default, providing:
- Detailed error messages
- Auto-reload on code changes
- Debug toolbar
- SQLAlchemy query logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.