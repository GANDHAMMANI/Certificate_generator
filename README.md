# Certificate Generator

This project is a Flask-based certificate generator designed to reduce the workload of teachers when issuing event certificates to students. Teachers can select a certificate template, upload a CSV with recipient names and emails, and the system will generate certificates in PDF format, sending them directly to each student's email. The project is especially useful for educational institutions for efficient certificate distribution post-events.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Template Selection:** Allows users to choose from multiple certificate templates, displayed in a card-style layout like an e-commerce platform.
- **Bulk Certificate Generation:** Generates certificates for multiple recipients provided in a CSV file.
- **PDF Conversion:** Converts generated certificate images to PDF format.
- **Email Delivery:** Sends certificates to recipients' emails in PDF format.
- **User Dashboard:** Provides an intuitive interface for template selection, CSV upload, and certificate generation.

## Default Credentials

- **Email:** `gandhammani2421@gmail.com`
- **Password:** `p123`
- **Note:** Users can change their password after logging in.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/certificate-generator.git
    cd certificate-generator
    ```

2. **Create and Activate Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**
    ```bash
    python -c "from app import db; db.create_all()"
    ```

5. **Configure Email Settings**
   - Update your email settings in `app.config` with your email provider's SMTP details.

## Usage

1. **Run the Application**
    ```bash
    flask run
    ```

2. **Access the Dashboard**
   - Open a web browser and navigate to `http://127.0.0.1:5000`.
   - Log in using the default credentials or register a new user.

3. **Select a Template and Upload CSV**
   - In the dashboard, choose a template by clicking on the desired template card.
   - Upload a CSV file with columns `Name` and `Email`.

4. **Generate and Send Certificates**
   - Click "Generate Certificates" to start the generation process.
   - Generated certificates will be stored in the `static/certificates` folder and emailed to recipients.

## Configuration

- **Template Files:** Add your certificate templates in the `static/templates` folder.
- **Font Settings:** Update font settings (like `FONT_PATH`, `FONT_SIZE`, and `Y_POSITION`) in the code as needed.
- **Render Deployment:** The project is deployed on Render. For deployment details, refer to the Render documentation.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.
