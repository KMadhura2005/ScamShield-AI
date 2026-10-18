
from flask import Flask, render_template, request, jsonify
import joblib
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "scamshield_dashboard.db"
MODEL_PATH = BASE_DIR / "models" / "scamshield_model.pkl"

# Load the trained machine learning model
model = joblib.load(MODEL_PATH)


# Initialize the dashboard database
def init_dashboard_db():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                risk_level TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


# Save one completed analysis
def save_analysis(risk_level):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            "INSERT INTO analysis_history (risk_level) VALUES (?)",
            (risk_level,)
        )


# Retrieve dashboard statistics
def get_dashboard_stats():
    with sqlite3.connect(DATABASE_PATH) as connection:
        total_checks = connection.execute(
            "SELECT COUNT(*) FROM analysis_history"
        ).fetchone()[0]

        high_risk_alerts = connection.execute(
            "SELECT COUNT(*) FROM analysis_history WHERE risk_level = ?",
            ("High",)
        ).fetchone()[0]

    return total_checks, high_risk_alerts


# Retrieve risk counts for the dashboard
def get_risk_counts():
    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute("""
            SELECT risk_level, COUNT(*)
            FROM analysis_history
            GROUP BY risk_level
        """).fetchall()

    counts = {"High": 0, "Medium": 0, "Low": 0}

    for risk_level, count in rows:
        if risk_level in counts:
            counts[risk_level] = count

    return counts


# Retrieve recent analyses
def get_recent_analyses():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("""
            SELECT id, risk_level, created_at
            FROM analysis_history
            ORDER BY id DESC
            LIMIT 5
        """).fetchall()

    return rows


# Warning signs and explanations
WARNING_RULES = {
    "Upfront payment demand": {
        "phrases": [
            "registration fee",
            "pay fee",
            "processing fee",
            "application fee",
            "refundable fee",
            "security deposit",
            "pay to confirm"
        ],
        "explanation": (
            "Requests for payment to secure a job may indicate a scam. "
            "Verify the employer independently before paying anything."
        ),
        "advice": (
            "Do not pay simply to secure selection. Confirm any legitimate "
            "charges directly with the employer through official channels."
        )
    },
    "Guaranteed selection": {
        "phrases": [
            "guaranteed job",
            "guaranteed selection",
            "100% selection",
            "direct joining without interview"
        ],
        "explanation": (
            "Promises of guaranteed selection without a credible hiring "
            "process can be a warning sign."
        ),
        "advice": (
            "Check the official careers page and confirm the recruitment "
            "process with the employer."
        )
    },
    "Unrealistic salary promise": {
        "phrases": [
            "easy money",
            "earn lakhs",
            "high salary with no experience",
            "earn thousands daily",
            "no work experience high salary"
        ],
        "explanation": (
            "Unusually high earnings for minimal work or no qualifications "
            "may be intended to attract applicants deceptively."
        ),
        "advice": (
            "Compare the advertised salary and responsibilities with "
            "similar roles and verify the offer."
        )
    },
    "Urgent pressure tactics": {
        "phrases": [
            "apply immediately",
            "limited seats",
            "last chance",
            "act now",
            "urgent payment",
            "offer expires today"
        ],
        "explanation": (
            "Artificial urgency can pressure applicants into acting "
            "before checking whether an offer is genuine."
        ),
        "advice": (
            "Take time to verify the company, recruiter, and offer before "
            "making a decision."
        )
    },
    "Sensitive information request": {
        "phrases": [
            "share your otp",
            "send your otp",
            "bank account details",
            "bank password",
            "send pan card",
            "send aadhaar",
            "share aadhaar"
        ],
        "explanation": (
            "Requests for OTPs, passwords, or sensitive financial details "
            "can expose applicants to identity theft or financial fraud."
        ),
        "advice": (
            "Never share OTPs or banking passwords. Verify any request "
            "for identity documents through official channels."
        )
    }
}


# Detect warning signs
def detect_warning_signs(text):
    text_lower = text.lower()
    warnings = []

    for title, rule in WARNING_RULES.items():
        matched_phrases = [
            phrase for phrase in rule["phrases"]
            if phrase in text_lower
        ]

        if matched_phrases:
            warnings.append({
                "title": title,
                "explanation": rule["explanation"],
                "advice": rule["advice"]
            })

    return warnings


# Find suspicious phrases
def find_suspicious_phrases(text):
    phrases = []

    for rule in WARNING_RULES.values():
        for phrase in rule["phrases"]:
            if phrase in text.lower() and phrase not in phrases:
                phrases.append(phrase)

    return phrases


# Assess risk level
def assess_risk(probability, warnings):
    # Preliminary project thresholds, not calibrated real-world probabilities.
    if probability >= 0.70 or len(warnings) >= 2:
        return "High", "high"

    if probability >= 0.30 or len(warnings) == 1:
        return "Medium", "medium"

    return "Low", "low"


# Recommendation based on risk level
def get_recommendation(risk_level):
    if risk_level == "High":
        return (
            "Pause before proceeding. Verify the employer independently "
            "and do not pay fees or share sensitive information until "
            "the opportunity is verified."
        )

    if risk_level == "Medium":
        return (
            "Proceed cautiously. Check the company's official careers "
            "website, recruiter identity, and hiring process."
        )

    return (
        "No strong warning was identified by this initial assessment. "
        "This does not prove the offer is genuine. Verify the employer "
        "before proceeding."
    )


# Analyze a job advertisement using the ML model
def analyze_job(job_text):
    probability = float(model.predict_proba([job_text])[0][1])
    prediction = int(model.predict([job_text])[0])

    warnings = detect_warning_signs(job_text)
    risk_level, risk_class = assess_risk(probability, warnings)

    return {
        "prediction": prediction,
        "probability": probability,
        "confidence": round(probability * 100, 1),
        "risk_level": risk_level,
        "risk_class": risk_class,
        "warnings": warnings,
        "suspicious_phrases": find_suspicious_phrases(job_text),
        "recommendation": get_recommendation(risk_level)
    }


# --------------------------------------------------
# HOME PAGE
# URL: /
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# --------------------------------------------------
# ABOUT PAGE
# URL: /about
# --------------------------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# --------------------------------------------------
# JOB ANALYSIS PAGE
# URL: /analyze
# --------------------------------------------------
@app.route("/analyze", methods=["GET", "POST"])
def analyze_page():
    job_text = ""
    analyzed = False
    error_message = None
    result = {}

    if request.method == "POST":
        job_text = request.form.get("job_description", "").strip()

        if len(job_text) < 80:
            error_message = (
                "Please enter a job description containing "
                "at least 80 characters."
            )
        else:
            job_text = job_text[:15000]

            try:
                result = analyze_job(job_text)
                analyzed = True
                save_analysis(result["risk_level"])

            except Exception:
                app.logger.exception("Website job analysis failed")
                error_message = (
                    "Analysis failed. Please check the Flask terminal."
                )

    return render_template(
        "analyze.html",
        job_text=job_text,
        analyzed=analyzed,
        error_message=error_message,
        prediction=result.get("prediction"),
        confidence=result.get("confidence"),
        warnings=result.get("warnings", []),
        risk_level=result.get("risk_level"),
        risk_class=result.get("risk_class"),
        recommendation=result.get("recommendation"),
        suspicious_phrases=result.get("suspicious_phrases", [])
    )


# --------------------------------------------------
# DASHBOARD PAGE
# URL: /dashboard
# --------------------------------------------------
@app.route("/dashboard")
def dashboard():
    total_checks, high_risk_alerts = get_dashboard_stats()
    risk_counts = get_risk_counts()
    recent_analyses = get_recent_analyses()

    return render_template(
        "index.html",
        prediction=None,
        confidence=None,
        warnings=[],
        risk_level=None,
        risk_class=None,
        recommendation=None,
        job_text="",
        analyzed=False,
        total_checks=total_checks,
        high_risk_alerts=high_risk_alerts,
        risk_counts=risk_counts,
        recent_analyses=recent_analyses
    )


# --------------------------------------------------
# CHROME EXTENSION API
# URL: /api/analyze
# --------------------------------------------------
@app.route("/api/analyze", methods=["POST"])
def analyze_api():
    data = request.get_json(silent=True) or {}
    job_text = data.get("job_description", "")

    if not isinstance(job_text, str) or not job_text.strip():
        return jsonify({
            "error": "Please provide a job advertisement to analyze."
        }), 400

    job_text = job_text.strip()

    if len(job_text) < 80:
        return jsonify({
            "error": "Please provide a more complete job listing."
        }), 400

    job_text = job_text[:15000]

    try:
        result = analyze_job(job_text)
        save_analysis(result["risk_level"])

        descriptions = {
            "High": (
                "Several risk indicators were identified. "
                "Verify this opportunity before proceeding."
            ),
            "Medium": (
                "Some indicators deserve further investigation."
            ),
            "Low": (
                "Few warning indicators were detected. "
                "The listing is not guaranteed to be genuine."
            )
        }

        return jsonify({
            "prediction": result["prediction"],
            "fraud_probability": result["confidence"],
            "risk_level": result["risk_level"],
            "risk_description": descriptions[result["risk_level"]],
            "warnings": result["warnings"],
            "suspicious_phrases": result["suspicious_phrases"],
            "recommendation": result["recommendation"]
        })

    except Exception:
        app.logger.exception("ScamShield AI analysis failed")
        return jsonify({
            "error": "Analysis failed. Check the Flask terminal."
        }), 500


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
