import os
import re
import uuid
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from flask_bcrypt import Bcrypt

from werkzeug.utils import secure_filename

from PyPDF2 import PdfReader
from docx import Document

from config import Config
from models import db, User, Report


# =======================================
# App Configuration
# =======================================

app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = "Please login to continue."


# =======================================
# Upload Folders
# =======================================

UPLOAD_FOLDER = "uploads"

RESUME_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "resume"
)

JD_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "jd"
)

os.makedirs(
    RESUME_FOLDER,
    exist_ok=True
)

os.makedirs(
    JD_FOLDER,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

app.config["RESUME_FOLDER"] = RESUME_FOLDER
app.config["JD_FOLDER"] = JD_FOLDER


# =======================================
# Database
# =======================================

db.init_app(app)

with app.app_context():

    db.create_all()


# =======================================
# Login Manager
# =======================================

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# =======================================
# Allowed File
# =======================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =======================================
# Extract Text
# =======================================

def extract_text(file_path):

    extension = (
        file_path
        .rsplit(
            ".",
            1
        )[1]
        .lower()
    )

    text = ""


    # --------------------------------
    # PDF
    # --------------------------------

    if extension == "pdf":

        reader = PdfReader(
            file_path
        )

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += (
                    page_text
                    + "\n"
                )


    # --------------------------------
    # DOCX
    # --------------------------------

    elif extension == "docx":

        document = Document(
            file_path
        )

        for paragraph in document.paragraphs:

            text += (
                paragraph.text
                + "\n"
            )


    # --------------------------------
    # TXT
    # --------------------------------

    elif extension == "txt":

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            text = file.read()


    return text


# =======================================
# ATS Skill Dictionary
# =======================================

SKILLS = {

    "python",
    "java",
    "c",
    "c++",
    "javascript",

    "html",
    "css",
    "react",
    "angular",
    "vue",

    "node.js",
    "express",

    "spring",
    "spring boot",

    "flask",
    "django",
    "fastapi",

    "mysql",
    "mongodb",
    "postgresql",
    "sqlite",
    "oracle",
    "sql",

    "aws",
    "azure",
    "gcp",

    "docker",
    "kubernetes",

    "git",
    "github",
    "linux",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",

    "nlp",
    "tensorflow",
    "pytorch",

    "opencv",
    "pandas",
    "numpy",
    "scikit-learn",

    "data analysis",
    "data science",

    "power bi",
    "tableau",

    "rest api",
    "api",

    "microservices",

    "problem solving",
    "communication",
    "teamwork",
    "leadership",
    "time management"
}


# =======================================
# Find Skills
# =======================================

def find_skills(text):

    text = text.lower()

    found = set()

    for skill in SKILLS:

        if skill.lower() in text:

            found.add(skill)

    return found


# =======================================
# Calculate ATS Score
# =======================================

def calculate_ats_score(
    resume_text,
    jd_text
):

    resume_skills = find_skills(
        resume_text
    )

    jd_skills = find_skills(
        jd_text
    )

    matched = (
        resume_skills
        .intersection(
            jd_skills
        )
    )

    missing = (
        jd_skills
        - resume_skills
    )


    # --------------------------------
    # Calculate Score
    # --------------------------------

    if len(jd_skills) == 0:

        score = 0

    else:

        score = round(
            (
                len(matched)
                /
                len(jd_skills)
            )
            * 100
        )


    return {

        "score": score,

        "matched": sorted(
            list(matched)
        ),

        "missing": sorted(
            list(missing)
        ),

        "resume_skills": sorted(
            list(resume_skills)
        ),

        "jd_skills": sorted(
            list(jd_skills)
        )
    }


# =======================================
# Generate Suggestions
# =======================================

def generate_suggestions(result):

    suggestions = []


    if result["score"] >= 90:

        suggestions.append(
            "Excellent! Your resume closely matches the job description."
        )

    elif result["score"] >= 75:

        suggestions.append(
            "Good match. Add the missing skills to further improve your ATS score."
        )

    elif result["score"] >= 50:

        suggestions.append(
            "Your resume partially matches the job description. Focus on the missing technical skills."
        )

    else:

        suggestions.append(
            "Your resume requires significant improvements to match the job requirements."
        )


    if len(result["missing"]) > 0:

        suggestions.append(
            "Missing Skills: "
            + ", ".join(
                result["missing"]
            )
        )


    if "communication" not in result["resume_skills"]:

        suggestions.append(
            "Include communication skills if you possess them."
        )


    if "teamwork" not in result["resume_skills"]:

        suggestions.append(
            "Mention teamwork or collaborative project experience."
        )


    if "problem solving" not in result["resume_skills"]:

        suggestions.append(
            "Highlight problem-solving experience using project examples."
        )


    return suggestions


# =======================================
# Extract Resume Details
# =======================================

def extract_resume_details(text):

    details = {

        "name": "Not Found",

        "email": "Not Found",

        "phone": "Not Found",

        "education": "Not Found"
    }


    # --------------------------------
    # Email
    # --------------------------------

    email = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if email:

        details["email"] = (
            email.group(0)
        )


    # --------------------------------
    # Phone
    # --------------------------------

    phone = re.search(
        r'(\+91[\s-]?)?[6-9]\d{9}',
        text
    )

    if phone:

        details["phone"] = (
            phone.group(0)
        )


    # --------------------------------
    # Name
    # --------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:

        details["name"] = lines[0]


    # --------------------------------
    # Education
    # --------------------------------

    education_keywords = [

        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "m.tech",
        "mtech",
        "master",
        "engineering",
        "computer science"
    ]

    for line in lines:

        line_lower = line.lower()

        if any(
            keyword in line_lower
            for keyword in education_keywords
        ):

            details["education"] = line

            break


    return details


# =======================================
# Home
# =======================================

@app.route("/")
def home():

    return redirect(
        url_for("login")
    )


# =======================================
# Login
# =======================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        user = User.query.filter_by(
            email=email
        ).first()


        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid Email or Password",
            "danger"
        )


    return render_template(
        "login.html"
    )


# =======================================
# Signup
# =======================================

@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )


        if (
            not full_name
            or not email
            or not password
            or not confirm_password
        ):

            flash(
                "Please fill all fields.",
                "danger"
            )

            return redirect(
                url_for("signup")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match!",
                "danger"
            )

            return redirect(
                url_for("signup")
            )


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "Email already exists!",
                "warning"
            )

            return redirect(
                url_for("signup")
            )


        hashed_password = (
            bcrypt
            .generate_password_hash(
                password
            )
            .decode("utf-8")
        )


        new_user = User(

            full_name=full_name,

            email=email,

            password=hashed_password
        )


        db.session.add(
            new_user
        )

        db.session.commit()


        flash(
            "Account created successfully! Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "signup.html"
    )


# =======================================
# Logout
# =======================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# =======================================
# Dashboard
# =======================================

@app.route(
    "/dashboard",
    methods=["GET", "POST"]
)
@login_required
def dashboard():

    result = None


    if request.method == "POST":

        resume = request.files.get(
            "resume"
        )

        jd = request.files.get(
            "job_description"
        )


        # --------------------------------
        # Check Files
        # --------------------------------

        if not resume or not jd:

            flash(
                "Please upload both Resume and Job Description.",
                "warning"
            )

            return redirect(
                url_for("dashboard")
            )


        if (
            resume.filename == ""
            or jd.filename == ""
        ):

            flash(
                "Please select both files.",
                "warning"
            )

            return redirect(
                url_for("dashboard")
            )


        # --------------------------------
        # Validate Extensions
        # --------------------------------

        if (
            not allowed_file(
                resume.filename
            )
            or
            not allowed_file(
                jd.filename
            )
        ):

            flash(
                "Only PDF, DOCX and TXT files are allowed.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )


        # --------------------------------
        # Original Filenames
        # --------------------------------

        original_resume_filename = (
            secure_filename(
                resume.filename
            )
        )

        original_jd_filename = (
            secure_filename(
                jd.filename
            )
        )


        # --------------------------------
        # Unique Filenames
        # --------------------------------

        resume_filename = (
            str(uuid.uuid4())
            + "_"
            + original_resume_filename
        )

        jd_filename = (
            str(uuid.uuid4())
            + "_"
            + original_jd_filename
        )


        # --------------------------------
        # File Paths
        # --------------------------------

        resume_path = os.path.join(
            app.config["RESUME_FOLDER"],
            resume_filename
        )

        jd_path = os.path.join(
            app.config["JD_FOLDER"],
            jd_filename
        )


        # --------------------------------
        # Save Files
        # --------------------------------

        resume.save(
            resume_path
        )

        jd.save(
            jd_path
        )


        # --------------------------------
        # Extract Text
        # --------------------------------

        resume_text = extract_text(
            resume_path
        )

        jd_text = extract_text(
            jd_path
        )


        # --------------------------------
        # Check Extracted Text
        # --------------------------------

        if not resume_text:

            flash(
                "Could not extract text from the resume.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )


        if not jd_text:

            flash(
                "Could not extract text from the job description.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )


        # --------------------------------
        # Calculate ATS Score
        # --------------------------------

        result = calculate_ats_score(
            resume_text,
            jd_text
        )


        # --------------------------------
        # Save Analysis Report
        # --------------------------------

        report = Report(

            user_id=current_user.id,

            resume_name=original_resume_filename,

            job_description_name=original_jd_filename,

            ats_score=int(
                result.get(
                    "score",
                    0
                )
            ),

            matched_skills=len(
                result.get(
                    "matched",
                    []
                )
            ),

            missing_skills=len(
                result.get(
                    "missing",
                    []
                )
            ),

            analysis_date=datetime.utcnow()
        )


        db.session.add(
            report
        )

        db.session.commit()


        # --------------------------------
        # Generate Suggestions
        # --------------------------------

        result["suggestions"] = (
            generate_suggestions(
                result
            )
        )


        # --------------------------------
        # Extract Resume Details
        # --------------------------------

        result["resume_details"] = (
            extract_resume_details(
                resume_text
            )
        )


        # --------------------------------
        # Success Message
        # --------------------------------

        flash(
            "ATS Analysis Completed Successfully!",
            "success"
        )


    return render_template(
        "dashboard.html",
        user=current_user,
        result=result
    )


# =======================================
# Upload Resume Page
# =======================================

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
@login_required
def upload():

    if request.method == "POST":

        if "resume" not in request.files:

            flash(
                "No file selected.",
                "danger"
            )

            return redirect(
                request.url
            )


        file = request.files[
            "resume"
        ]


        if file.filename == "":

            flash(
                "Please choose a resume.",
                "warning"
            )

            return redirect(
                request.url
            )


        if not allowed_file(
            file.filename
        ):

            flash(
                "Only PDF, DOCX and TXT files are allowed.",
                "danger"
            )

            return redirect(
                request.url
            )


        filename = secure_filename(
            file.filename
        )


        filepath = os.path.join(
            app.config["RESUME_FOLDER"],
            filename
        )


        file.save(
            filepath
        )


        flash(
            "Resume uploaded successfully!",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "upload.html",
        user=current_user
    )


# =======================================
# Reports
# =======================================

@app.route("/reports")
@login_required
def reports():

    reports = Report.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Report.analysis_date.desc()
    ).all()


    return render_template(
        "reports.html",
        user=current_user,
        reports=reports
    )
@app.route("/report/<int:report_id>")
@login_required
def view_report(report_id):

    report = Report.query.filter_by(
        id=report_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "report_details.html",
        user=current_user,
        report=report
    )

# =======================================
# Change Password
# =======================================

@app.route(
    "/change-password",
    methods=["POST"]
)
@login_required
def change_password():

    current_password = request.form.get(
        "current_password",
        ""
    )

    new_password = request.form.get(
        "new_password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )


    if not bcrypt.check_password_hash(
        current_user.password,
        current_password
    ):

        flash(
            "Current password is incorrect.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )


    if len(new_password) < 6:

        flash(
            "New password must contain at least 6 characters.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )


    if new_password != confirm_password:

        flash(
            "New passwords do not match.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )


    current_user.password = (
        bcrypt
        .generate_password_hash(
            new_password
        )
        .decode("utf-8")
    )


    db.session.commit()


    flash(
        "Password changed successfully!",
        "success"
    )


    return redirect(
        url_for("settings")
    )


# =======================================
# Settings
# =======================================

@app.route("/settings")
@login_required
def settings():

    return render_template(
        "settings.html",
        user=current_user
    )


# =======================================
# Run Application
# =======================================

if __name__ == "__main__":

    app.run(
        debug=True
    )