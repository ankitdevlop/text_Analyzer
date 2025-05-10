from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from forms import LoginForm, RegistrationForm, TextAnalysisForm
from models import User, TextEntry
import math


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TextAnalysisForm()
    
    if form.validate_on_submit():
        # Calculate metrics
        content = form.content.data
        word_count = len(content.split())
        char_count = len(content)
        # Assuming average reading speed of 200 words per minute
        reading_time = word_count / 200.0
        
        # Create and save new text entry
        text_entry = TextEntry(
            content=content,
            word_count=word_count,
            char_count=char_count,
            reading_time=reading_time,
            font_style=form.font_style.data,
            background_color=form.background_color.data,
            user_id=current_user.id
        )
        db.session.add(text_entry)
        db.session.commit()
        flash('Text saved successfully!', 'success')
    
    # Get user's saved text entries
    text_entries = TextEntry.query.filter_by(user_id=current_user.id).order_by(TextEntry.created_at.desc()).all()
    
    return render_template('dashboard.html', title='Dashboard', form=form, text_entries=text_entries)


@app.route('/analyze-text', methods=['POST'])
@login_required
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    # Basic text analysis
    word_count = len(text.split())
    char_count = len(text)
    reading_time = math.ceil(word_count / 200.0)  # Average reading speed of 200 wpm
    
    return jsonify({
        'wordCount': word_count,
        'charCount': char_count,
        'readingTime': reading_time
    })


@app.route('/delete-entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = TextEntry.query.get_or_404(entry_id)
    
    # Ensure only the owner can delete their entries
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Text entry deleted successfully!', 'success')
    return redirect(url_for('dashboard'))
