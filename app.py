from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import datetime
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"] 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)

@app.route("/dbtest")
def dbtest():
    return str(db.engine.execute("select 1").fetchone())
# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Sample blog posts
def create_sample_posts():
    posts = [
        BlogPost(title="Welcome to our NEW platform!", 
                content="This is our first blog post. Welcome to our community!"),
        BlogPost(title="New features coming soon", 
                content="We're working on exciting new features that will be released next month."),
        BlogPost(title="Community guidelines", 
                content="Please read our updated community guidelines to ensure a positive experience for everyone."),
    ]
    for post in posts:
        if not BlogPost.query.filter_by(title=post.title).first():
            db.session.add(post)
    db.session.commit()

# Mock SMS sending function (in a real app, you would integrate with a service like Twilio)
def send_sms(phone, code):
    print(f"[MOCK SMS] Verification code for {phone}: {code}")
    # In production, replace with actual SMS integration
    return True

# Routes
@app.route('/')
def index():
    if 'userid' in session:
        # User is logged in, show dashboard with blog posts
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        return render_template('dashboard.html', userid=session['userid'], posts=posts)
    else:
        # User is not logged in, show default page
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        phone = request.form['phone']
        
        # Check if userid already exists
        if User.query.filter_by(userid=userid).first():
            flash('User ID already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(userid=userid, password_hash=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        
        user = User.query.filter_by(userid=userid).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['userid'] = userid
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid user ID or password.', 'error')
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        userid = request.form['userid']
        
        user = User.query.filter_by(userid=userid).first()
        
        if user:
            # Generate verification code
            code = str(random.randint(100000, 999999))
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
            
            # Save verification code
            verification = VerificationCode(userid=userid, code=code, expires_at=expires_at)
            db.session.add(verification)
            db.session.commit()
            
            # Send SMS (mock implementation)
            send_sms(user.phone, code)
            
            session['reset_userid'] = userid
            flash('Verification code sent to your phone.', 'success')
            return redirect(url_for('verify_code'))
        else:
            flash('User ID not found.', 'error')
    
    return render_template('forgot_password.html')

@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if 'reset_userid' not in session:
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        code = request.form['code']
        
        # Find valid verification code
        verification = VerificationCode.query.filter_by(
            userid=session['reset_userid'], 
            code=code,
            used=False
        ).first()
        
        if verification and verification.expires_at > datetime.now(timezone.utc):
            # Mark code as used
            verification.used = True
            db.session.commit()
            
            session['verified'] = True
            flash('Verification successful. You can now reset your password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Invalid or expired verification code.', 'error')
    
    return render_template('verify_code.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_userid' not in session or 'verified' not in session:
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('reset_password'))
        
        # Update user password
        user = User.query.filter_by(userid=session['reset_userid']).first()
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        
        # Clear reset session
        session.pop('reset_userid', None)
        session.pop('verified', None)
        
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Initialize database and create sample data
with app.app_context():
    db.create_all()
    create_sample_posts()


if __name__ == '__main__':
    app.run(debug=True)

