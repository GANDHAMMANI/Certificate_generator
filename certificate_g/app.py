import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image, ImageDraw, ImageFont
from flask_mail import Mail, Message

# Initialize Flask app and database
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'gandhamsaketh073@gmail.com'
app.config['MAIL_PASSWORD'] = 'oyad zwxr txuv wpgi'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

# Ensure the folder for certificates exists
if not os.path.exists('static/certificates'):
    os.makedirs('static/certificates')

# Path to the certificate template and font
TEMPLATE_PATH = "static/template.png"
FONT_PATH = "static/times new roman italic.ttf"
FONT_SIZE = 100
Y_POSITION = 700

# User model (for the predefined user)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Hardcoded credentials for a single user
HARD_CODED_EMAIL = 'gandhammani2421@gmail.com'
HARD_CODED_PASSWORD = generate_password_hash('p123', method='pbkdf2:sha256')  # Change this password as needed

# Flask-Login loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check against hardcoded credentials
        if email == HARD_CODED_EMAIL and check_password_hash(HARD_CODED_PASSWORD, password):
            # Create a user object dynamically
            user = User(id=1, email=email, password=HARD_CODED_PASSWORD)  # Dummy user instance
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Login failed. Check your credentials and try again.')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)

@app.route('/generate', methods=['POST'])
@login_required
def generate_certificates():
    # Get the selected template from the form (passed via hidden input)
    selected_template = request.form.get('template')

    # Check if the file is in the request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        # Path to the selected template
        template_path = f"static/templates/{selected_template}"

        # Read the CSV file
        names_df = pd.read_csv(file)

        for index, row in names_df.iterrows():
            name = row['Name']
            png_path = f"static/certificates/certificate_{name.replace(' ', '_')}.png"
            pdf_path = f"static/certificates/certificate_{name.replace(' ', '_')}.pdf"

            # Generate PNG certificate
            img = Image.open(template_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
            text_width, text_height = draw.textsize(name, font=font)
            image_width = img.width
            x_position = (image_width - text_width) / 2
            draw.text((x_position, Y_POSITION), name, font=font, fill="black")
            img.save(png_path)

            # Convert PNG to PDF
            image = Image.open(png_path)
            rgb_image = image.convert('RGB')
            rgb_image.save(pdf_path, "PDF", resolution=100.0)

            # Send the PDF certificate via email
            send_certificate_via_email(name, pdf_path, row['Email'])

        flash('Certificates generated and sent successfully!')
        return redirect(url_for('download_page'))


def send_certificate_via_email(name, certificate_path, recipient_email):
    msg = Message('Your Certificate of Appreciation', sender='gandhamsaketh073@gmail.com', recipients=[recipient_email])

    # Email content
    msg.html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Certificate</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .footer {{
                margin-top: 20px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
            }}
            .icon {{
                width: 40px;
                height: 40px;
                vertical-align: middle;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Certificate of Appreciation</h1>
               
            </div>
            <p>Dear {name},</p>
            <p>Congratulations! We are pleased to inform you that you have been awarded a certificate of appreciation.</p>
            <p>Please find your certificate attached below.</p>
            <div class="footer">
                <p>Best Regards,<br>Your Organization Name</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Attach the PDF certificate
    with app.open_resource(certificate_path) as fp:
        msg.attach(f"certificate_{name}.pdf", "application/pdf", fp.read())

    # Send the email
    mail.send(msg)



@app.route('/download')
@login_required
def download_page():
    # List only PDF files from the certificates directory
    certificates = [file for file in os.listdir('static/certificates') if file.endswith('.pdf')]
    return render_template('download.html', certificates=certificates)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database within app context
    app.run(debug=True)
