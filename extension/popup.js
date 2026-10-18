
const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeTextBtn = document.getElementById("analyzeTextBtn");
const jobDescription = document.getElementById("jobDescription");
const status = document.getElementById("status");
const results = document.getElementById("results");

const API_URL = "http://127.0.0.1:5000/api/analyze";

async function analyzeJob(text) {
    if (!text || !text.trim()) {
        status.textContent = "Please paste a job description.";
        results.hidden = true;
        return;
    }

    if (text.trim().length < 80) {
        status.textContent = "Please enter at least 80 characters.";
        results.hidden = true;
        return;
    }

    status.textContent = "Analyzing job description...";
    results.hidden = true;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                job_description: text.trim().slice(0, 15000)
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        showResults(data);
        status.textContent = "Analysis completed.";
    } catch (error) {
        status.textContent =
            error.message || "Could not connect to the Flask server.";
    }
}

function showResults(data) {
    saveAnalysisHistory(data);
    results.hidden = false;

    document.getElementById("riskLevel").textContent =
        data.risk_level || "Unknown";

    document.getElementById("riskDescription").textContent =
        data.risk_description || "";

    document.getElementById("fraudProbability").textContent =
        `${data.fraud_probability ?? 0}%`;

    document.getElementById("recommendation").textContent =
        data.recommendation ||
        "Verify the employer independently.";

    // Display the risk level.
    const riskCard = document.getElementById("riskCard");

    riskCard.classList.remove(
        "high-risk",
        "medium-risk",
        "low-risk"
    );

    const classes = {
        High: "high-risk",
        Medium: "medium-risk",
        Low: "low-risk"
    };

    riskCard.classList.add(
        classes[data.risk_level] || "medium-risk"
    );

    // Display warning signs.
    const warningList = document.getElementById("warningList");
    warningList.replaceChildren();

    if (Array.isArray(data.warnings) && data.warnings.length > 0) {
        data.warnings.forEach((warning) => {
            const item = document.createElement("li");

            const title = document.createElement("strong");
            title.textContent = warning.title || "Warning sign";
            item.appendChild(title);

            if (warning.explanation) {
                const explanation = document.createElement("p");
                explanation.textContent = warning.explanation;
                item.appendChild(explanation);
            }

            if (warning.advice) {
                const advice = document.createElement("p");
                advice.textContent = `Advice: ${warning.advice}`;
                item.appendChild(advice);
            }

            warningList.appendChild(item);
        });
    } else {
        const item = document.createElement("li");
        item.textContent =
            "No keyword-based warning signs were detected.";
        warningList.appendChild(item);
    }

    // Display suspicious phrases.
    const phrasesContainer =
        document.getElementById("suspiciousPhrases");

    if (phrasesContainer) {
        phrasesContainer.replaceChildren();

        const phrases = Array.isArray(data.suspicious_phrases)
            ? data.suspicious_phrases
            : [];

        if (phrases.length > 0) {
            phrases.forEach((phrase) => {
                const tag = document.createElement("span");

                tag.className = "suspicious-phrase";
                tag.textContent = phrase;

                phrasesContainer.appendChild(tag);
            });
        } else {
            phrasesContainer.textContent =
                "No suspicious phrases detected.";
        }
    }
}

// Analyze pasted job descriptions.
analyzeTextBtn.addEventListener("click", () => {
    analyzeJob(jobDescription.value);
});

// Analyze the currently open webpage.
analyzeBtn.addEventListener("click", async () => {
    status.textContent = "Reading current webpage...";
    results.hidden = true;

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if (
            !tab ||
            !tab.id ||
            !tab.url ||
            tab.url.startsWith("chrome://") ||
            tab.url.startsWith("chrome-extension://") ||
            tab.url.startsWith(
                "https://chromewebstore.google.com/"
            )
        ) {
            throw new Error(
                "Open a regular webpage and try again."
            );
        }

        const extracted = await chrome.scripting.executeScript({
            target: {
                tabId: tab.id
            },
            func: () => ({
                title: document.title,
                text: document.body?.innerText || ""
            })
        });

        const page = extracted?.[0]?.result;

        if (!page || !page.text.trim()) {
            throw new Error(
                "No readable text found on this webpage."
            );
        }

        const pageText =
            `${page.title}\n\n${page.text}`.slice(0, 15000);

        await analyzeJob(pageText);
    } catch (error) {
        status.textContent =
            error.message || "Could not read this webpage.";
    }
});

const copyReportBtn = document.getElementById("copyReportBtn");
const copyStatus = document.getElementById("copyStatus");

if (copyReportBtn) {
    copyReportBtn.addEventListener("click", async () => {
        const riskLevel =
            document.getElementById("riskLevel")?.textContent || "Unknown";

        const fraudProbability =
            document.getElementById("fraudProbability")?.textContent || "N/A";

        const riskDescription =
            document.getElementById("riskDescription")?.textContent || "";

        const recommendation =
            document.getElementById("recommendation")?.textContent || "";

        const warningItems = [
            ...document.querySelectorAll("#warningList li")
        ].map(item => item.innerText.trim());

        const suspiciousPhrases = [
            ...document.querySelectorAll("#suspiciousPhrases .suspicious-phrase")
        ].map(item => item.textContent.trim());

        const report = [
            "SCAMSHIELD AI - JOB ANALYSIS REPORT",
            "-----------------------------------",
            `Risk Level: ${riskLevel}`,
            `Estimated Fraud Probability: ${fraudProbability}`,
            `Risk Description: ${riskDescription}`,
            "",
            "WARNING SIGNS:",
            ...(warningItems.length ? warningItems : ["None listed"]),
            "",
            "SUSPICIOUS PHRASES:",
            ...(suspiciousPhrases.length
                ? suspiciousPhrases
                : ["None detected"]),
            "",
            "RECOMMENDATION:",
            recommendation,
            "",
            "Note: This is an automated estimate, not proof of fraud."
        ].join("\n");

        try {
            await navigator.clipboard.writeText(report);
            copyStatus.textContent = "Report copied successfully!";
        } catch (error) {
            copyStatus.textContent =
                "Copy failed. Please try again.";
        }
    });
}



const historyList = document.getElementById("historyList");
const historyEmpty = document.getElementById("historyEmpty");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

const HISTORY_KEY = "scamShieldAnalysisHistory";
const MAX_HISTORY = 5;

function displayHistory() {
    chrome.storage.local.get([HISTORY_KEY], (result) => {
        const history = result[HISTORY_KEY] || [];

        historyList.replaceChildren();

        historyEmpty.hidden = history.length > 0;

        history.forEach((entry) => {
            const item = document.createElement("li");
            const title = document.createElement("strong");
            const details = document.createElement("p");
            const date = document.createElement("small");

            title.textContent = entry.riskLevel;
            details.textContent =
                `Fraud probability: ${entry.probability}%`;
            date.textContent = entry.date;

            item.append(title, details, date);
            historyList.appendChild(item);
        });
    });
}

function saveAnalysisHistory(data) {
    chrome.storage.local.get([HISTORY_KEY], (result) => {
        const history = result[HISTORY_KEY] || [];

        history.unshift({
            riskLevel: data.risk_level || "Unknown",
            probability: data.fraud_probability ?? 0,
            date: new Date().toLocaleString()
        });

        chrome.storage.local.set({
            [HISTORY_KEY]: history.slice(0, MAX_HISTORY)
        }, displayHistory);
    });
}

if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener("click", () => {
        chrome.storage.local.remove(HISTORY_KEY, displayHistory);
    });
}

displayHistory();
