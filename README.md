
# 🛡️ ScamShield AI — AI-Powered Job Scam Detection

ScamShield AI is a machine learning-based application that helps job seekers identify potential warning signs in online job advertisements. It combines a Flask web application, a risk-analysis dashboard, and a Chrome extension to make job scam analysis more accessible.

> **Project goal:** Help users make more informed decisions by identifying suspicious language and potential job scam indicators.

## ✨ Features

- **AI-Based Detection:** Analyzes job advertisement text using a trained machine learning model.
- **Risk Classification:** Displays a Low, Medium, or High risk category.
- **Suspicious Phrase Detection:** Highlights potentially misleading or suspicious wording.
- **Safety Warnings:** Checks for indicators such as upfront payment requests, guaranteed selection claims, unrealistic salary promises, and urgency tactics.
- **Web Dashboard:** Displays analysis statistics, risk summaries, and recent analysis history.
- **Analysis History:** Stores analysis records locally using SQLite.
- **Chrome Extension:** Provides browser-based job text analysis through the Flask API.
- **Report Copying:** Supports copying analysis reports from the extension.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web application and API |
| Scikit-learn | Machine learning |
| HTML5 and CSS3 | User interface |
| JavaScript | Browser extension functionality |
| SQLite | Local analysis history |
| Chrome Extension APIs | Browser integration |

## 📁 Project Structure

```text
ScamShield-AI/
├── app.py
├── train_model.py
├── requirements.txt
├── .gitignore
├── README.md
├── models/
│   └── scamshield_model.pkl
├── templates/
│   ├── home.html
│   ├── about.html
│   ├── analyze.html
│   └── index.html
├── static/
│   └── style.css
└── extension/
    ├── manifest.json
    ├── popup.html
    ├── popup.css
    └── popup.js
```

The local training dataset and SQLite database are excluded from version control.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version for the project's dependencies
- Google Chrome, if you want to use the extension
- Git

### 1. Clone the repository

```bash
git clone https://github.com/KMadhura2005/ScamShield-AI.git
cd ScamShield-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the application

```bash
python app.py
```

Open your browser at:

http://127.0.0.1:5000

Keep the Flask server running while using the local application.

## 🧩 Chrome Extension Setup

1. Start the Flask application.
2. Open Google Chrome.
3. Visit `chrome://extensions/`.
4. Enable **Developer mode**.
5. Click **Load unpacked**.
6. Select the project's `extension` folder.
7. Open the extension and try analyzing job-related text.

The extension relies on the local Flask API for analysis. Confirm that its API address matches the address and port used by the running application.

## 🔍 How It Works

1. **Input:** Provide the text of a job advertisement.
2. **Analysis:** The machine learning model and warning checks examine the text.
3. **Risk assessment:** The application presents its prediction and risk classification.
4. **Review:** Read the detected warning signals and independently verify the employer.

## ⚠️ Disclaimer

ScamShield AI is an educational and decision-support project. Its predictions, risk scores, and warning rules are estimates and may be incorrect. A low-risk result does not guarantee that a job is genuine, and a high-risk result does not prove fraud.

Always verify employers through official channels. Be cautious of recruitment fees, unrealistic promises, and requests for sensitive personal or financial information.

## 🚀 Future Improvements

- Evaluate model performance on unseen advertisements.
- Improve precision and recall for fraudulent-job detection.
- Expand and maintain the training dataset.
- Improve the dashboard and analysis reports.
- Explore secure online deployment.

## 👩‍💻 Developer

**GitHub:** [KMadhura2005](https://github.com/KMadhura2005)

---

*Built to support safer and more informed job searching.*
