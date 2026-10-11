# ResumeXpert – AI Resume Analyzer

ResumeXpert is a web-based resume analysis application built using Python and Flask. It helps users compare their resumes with job descriptions and identify matching skills, missing skills, and areas for improvement.

## Features

- User registration and login
- Resume and job description uploads
- PDF, DOCX, and TXT file support
- Resume text extraction
- Skill matching and ATS-style score calculation
- Matched and missing skills identification
- Resume improvement suggestions
- Saved analysis reports
- Account settings and password management

## Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite, SQLAlchemy
- **Authentication:** Flask-Login
- **Password Hashing:** Flask-Bcrypt
- **Document Processing:** PyPDF2, python-docx

## How It Works

1. Register or log in.
2. Upload your resume.
3. Provide the job description.
4. The application extracts text from both documents.
5. The system identifies matching and missing skills.
6. An ATS-style score and suggestions are displayed.
7. Review saved reports when needed.

## Installation

Clone the repository:

```bash
git clone https://github.com/dpavani2976-hub/ResumeXpert.git
cd ResumeXpert/ResumeXpert
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the local URL shown in your terminal.

## Project Structure

```text
ResumeXpert/
├── static/
│   ├── css/
│   └── js/
├── templates/
├── app.py
├── config.py
├── models.py
├── requirements.txt
└── .gitignore
```

## Limitations

- Skill matching relies on predefined keywords and rules.
- The ATS-style score is an estimate and may differ from real applicant tracking systems.
- Analysis quality depends on the content and formatting of uploaded documents.

## Future Enhancements

- Machine learning-based resume analysis
- Expanded skill databases
- More personalized resume improvement suggestions
- Online deployment

## Author

Developed as a Python Flask project.
