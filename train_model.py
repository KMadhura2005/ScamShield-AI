
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# File paths
DATA_PATH = "data/fake_job_postings.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "scamshield_model.pkl")

# Create the models folder if it does not exist
os.makedirs(MODEL_DIR, exist_ok=True)

# Load the dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Select useful text columns that exist in the dataset
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

available_columns = [
    column for column in text_columns if column in df.columns
]

# Combine the text fields
df[available_columns] = df[available_columns].fillna("")

df["combined_text"] = df[available_columns].agg(" ".join, axis=1)

# Remove rows without useful text
df = df[df["combined_text"].str.strip().ne("")]

# Prepare features and labels
X = df["combined_text"]
y = df["fraudulent"].astype(int)

print(f"Total usable postings: {len(df)}")
print("\nClass distribution:")
print(y.value_counts())

# Split the data while preserving the class proportions
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Build the text classification pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            max_features=50000,
            ngram_range=(1, 2),
            min_df=2
        )
    ),
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        )
    )
])

# Train the model
print("\nTraining ScamShield AI...")
model.fit(X_train, y_train)

# Evaluate the model on unseen test data
predictions = model.predict(X_test)

print("\nModel evaluation")
print("----------------")
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Legitimate", "Fraudulent"],
        zero_division=0
    )
)

print("Confusion matrix:")
print(confusion_matrix(y_test, predictions))

# Save the trained pipeline
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully: {MODEL_PATH}")
