import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db, login_manager
from models import User, Attendance
from forms import LoginForm, RegistrationForm
from face_utils import process_image_for_face_recognition
import logging

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Save the face photo
            photo = form.face_photo.data
            filename = secure_filename(f"{form.username.data}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            
            # Process face photo for encoding
            face_encoding = process_image_for_face_recognition(photo_path)
            if face_encoding is None:
                flash('No face detected in the photo. Please try again.', 'danger')
                os.remove(photo_path)
                return render_template('register.html', form=form)
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                face_encoding=face_encoding
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
            
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get attendance statistics
    user_attendance = Attendance.query.filter_by(user_id=current_user.id).all()
    stats = {
        'present': sum(1 for a in user_attendance if a.status == 'present'),
        'late': sum(1 for a in user_attendance if a.status == 'late'),
        'absent': sum(1 for a in user_attendance if a.status == 'absent')
    }
    
    # Get recent attendance records
    recent_attendance = Attendance.query.filter_by(user_id=current_user.id)\
        .order_by(Attendance.timestamp.desc())\
        .limit(5)\
        .all()
        
    return render_template('dashboard.html', 
                         stats=stats,
                         recent_attendance=recent_attendance)

@app.route('/attendance')
@login_required
def attendance():
    # Get today's attendance status
    today = datetime.utcnow().date()
    today_status = Attendance.query.filter_by(user_id=current_user.id)\
        .filter(db.func.date(Attendance.timestamp) == today)\
        .first()
        
    return render_template('attendance.html', today_status=today_status)

@app.route('/view_history')
@login_required
def view_history():
    # Get all attendance records for the current user
    attendance_records = Attendance.query.filter_by(user_id=current_user.id)\
        .order_by(Attendance.timestamp.desc())\
        .paginate(page=request.args.get('page', 1, type=int), per_page=10)

    return render_template('view_history.html', 
                         attendance_records=attendance_records)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500