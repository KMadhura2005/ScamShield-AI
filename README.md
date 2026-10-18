# 🛡️ ScamShield AI — Job Scam Detector

ScamShield AI is a machine learning–powered application designed to help users identify potential job scams by analyzing job advertisements and highlighting suspicious indicators.

## 🚀 Features

- **Job Advertisement Analysis:** Analyze job descriptions to identify potential scam indicators.
- **ML-Based Prediction:** Uses a trained machine learning model to estimate potential fraud risk.
- **Risk Assessment:** Displays a risk level and fraud score.
- **Warning Signs:** Highlights suspicious phrases and potential red flags.
- **Dashboard:** Stores analysis history for reviewing previous results.
- **Chrome Extension:** Analyze job listings directly from supported webpages.
- **Input Validation:** Provides feedback when the advertisement field is empty.

## 🧰 Technologies Used

- Python
- Flask
- Machine Learning
- Scikit-learn
- SQLite
- HTML and CSS
- JavaScript
- Chrome Extension APIs
- Render

## 🌐 Live Demo

**Web Application:** https://scamshield-ai-0aa0.onrender.com

**GitHub Repository:** https://github.com/KMadhura2005/ScamShield-AI

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/KMadhura2005/ScamShield-AI.git
cd ScamShield-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the repository includes `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open the local URL shown in your terminal.

## 🧩 Chrome Extension Setup

1. Open Google Chrome.
2. Visit `chrome://extensions`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the repository's `extension` folder.
6. Open the ScamShield AI extension and test it on a job listing.

## ⚙️ How It Works

1. The user submits a job advertisement or analyzes a listing through the extension.
2. The application processes the available job text.
3. The trained model predicts a potential fraud risk.
4. The application displays the risk assessment and relevant warning signs.
5. Analysis history can be reviewed through the dashboard.

## 🎯 Project Goal

To help job seekers recognize suspicious recruitment practices and make more informed decisions when evaluating job opportunities.

## ⚠️ Disclaimer

ScamShield AI is an assistance tool, not a guarantee that a job is genuine or fraudulent. Predictions may be incorrect. Verify employers, recruitment channels, and payment requests independently before sharing sensitive information or making payments.

## 👩‍💻 Author

**Madhura Kadam**

Computer Science and Engineering Student

GitHub: https://github.com/KMadhura2005
