# 🛡️ ScamShield AI — AI-Powered Job Scam Detection

ScamShield AI is a machine learning-based project designed to help users identify potentially fraudulent job advertisements. It combines a Flask web application with a Chrome extension to make job scam analysis more accessible.

## ✨ Features

- **AI-Based Detection:** Analyzes job descriptions using a trained machine learning model.
- **Risk Classification:** Categorizes job advertisements as Low, Medium, or High Risk.
- **Suspicious Phrase Detection:** Highlights potentially misleading or suspicious language.
- **Safety Warnings:** Flags common scam indicators, such as upfront payment requests, guaranteed selection claims, unrealistic salaries, and urgency tactics.
- **Web Dashboard:** Displays analysis statistics, risk distribution, and recent analyses.
- **Chrome Extension:** Allows users to analyze job-related text and view results from the browser.
- **Analysis History:** Maintains recent analysis records and dashboard statistics.
- **Report Copying:** Allows users to copy an analysis report from the extension.

## 🧰 Technologies Used

- Python
- Flask
- Machine Learning
- Scikit-learn
- HTML5
- CSS3
- JavaScript
- SQLite
- Chrome Extension APIs

## 📁 Project Structure

```text
ScamShield-AI/
├── app.py
├── train_model.py
├── requirements.txt
├── .gitignore
├── models/
│   └── scamshield_model.pkl
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── extension/
    ├── manifest.json
    ├── popup.html
    ├── popup.css
    └── popup.js
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KMadhura2005/ScamShield-AI.git
cd ScamShield-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

`http://127.0.0.1:5000`

## 🧩 Chrome Extension Setup

1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the `extension` folder inside the cloned project.
6. Open the extension and try analyzing job-related text.

**Note:** The extension communicates with the Flask application, so start the Flask server before using features that require the local API.

## 🛡️ Important Disclaimer

ScamShield AI provides an estimated risk assessment, not a definitive judgment about whether a job advertisement is fraudulent. Machine learning predictions and warning rules can produce false positives or miss scams. Always verify employers through official channels, and never pay recruitment fees or share sensitive information with unverified parties.

## 🚀 Future Improvements

- Expand and improve the training dataset.
- Evaluate model performance on unseen job advertisements.
- Improve detection of new and evolving scam patterns.
- Enhance the user interface and reporting features.
- Explore deployment options for online access.

## 👩‍💻 Developer

**GitHub:** [KMadhura2005](https://github.com/KMadhura2005)

---

*Built to support safer and more informed job searching.*