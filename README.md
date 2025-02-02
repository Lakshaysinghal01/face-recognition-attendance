# Face Recognition Attendance Management System

A comprehensive web-based attendance management system that uses facial recognition technology for automated attendance tracking. Built with Flask and OpenCV, this system provides a secure and efficient way to manage attendance records.

## Features

- 👤 Face Recognition-based attendance marking
- 📸 Support for both webcam capture and photo upload
- 🔐 Secure user authentication system
- 📊 Attendance history and statistics
- 📱 Responsive web interface
- 👨‍💼 Admin dashboard for attendance management
- 📅 Daily, weekly, and monthly attendance reports
- 🕒 Automatic status tracking (Present/Late)

## Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Face Recognition**: OpenCV with Haar Cascade
- **Frontend**: Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **ORM**: SQLAlchemy

## Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Webcam (for live capture)

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd face-recognition-attendance
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Required environment variables
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@host:port/database
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
├── app.py              # Flask application initialization
├── auth.py            # Authentication related functions
├── face_utils.py      # Face recognition utilities
├── forms.py           # Form definitions
├── models.py          # Database models
├── routes.py          # Route handlers
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
└── uploads/          # Uploaded images directory
```

## Usage Guide

### Registration

1. Click on "Register" in the navigation bar
2. Fill in your details (username, email, password)
3. Upload a clear front-facing photo for face recognition
4. Submit the registration form

### Marking Attendance

1. Login to your account
2. Navigate to "Mark Attendance"
3. Choose either:
   - Use webcam to capture your face
   - Upload a photo manually
4. The system will verify your face and mark attendance
5. Attendance status (Present/Late) is automatically determined based on time

### Viewing Attendance

1. Go to "Dashboard" to see attendance statistics
2. Use "View History" for detailed attendance records
3. Admins can access the "Reports" section for comprehensive reports

## API Endpoints

- `/api/mark-attendance` (POST) - Mark attendance with face photo
- `/api/attendance-status` (GET) - Get current day's attendance status

## Security Features

- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Secure file upload handling
- JWT-based API authentication
- Session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
