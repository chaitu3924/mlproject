from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store1.db'
app.secret_key = 'sqlalchemy'
db = SQLAlchemy(app)

# Database Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aadhar = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_correct_password(self, password):
        return check_password_hash(self.password, password)

# Routes
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        aadhar = request.form.get('aadhar')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(aadhar=aadhar, email=email).first()
        if user and user.is_correct_password(password):
            session.permanent = True
            session['user'] = user.email  # Store user's email (or any unique identifier)
            return redirect(url_for('afterlogin'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/afterlogin')
def afterlogin():
    return render_template('afterlogin.html')
    
@app.route('/certificate')
def certificate():
    return render_template('certificate.html')

@app.route('/issuance')
def issuance():
    return render_template('issuance.html')
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        aadhar = request.form.get('aadhar')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        phone = request.form.get('phone')

        if password != confirm:
            return "Passwords do not match", 400

        # Check if user already exists by Aadhar or Email
        existing_user = User.query.filter((User.aadhar == aadhar) | (User.email == email)).first()
        if existing_user:
            return "Aadhar or Email already exists", 400

        # Add new user to the database
        new_user = User(aadhar=aadhar, email=email, phone=phone)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    # Initialize the database (uncomment this for first-time use)
    with app.app_context():
        db.create_all()
        app.run(debug=True)

