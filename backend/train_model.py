import pandas as pd
import joblib

from training_data import training_data

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Create DataFrame
df = pd.DataFrame(training_data, columns=["text", "label"])

# Convert text to TF-IDF vectors
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(df["text"])

# Train classifier
model = LogisticRegression(max_iter=1000)

model.fit(X, df["label"])

print("Model trained successfully")

# Test queries
test_queries = [
    "Narendra Modi is the Prime Minister of India",
    "Earth is flat",
    "Python is the best language",
    "Who won the 2022 FIFA World Cup?",
    "Mount Everest is the tallest mountain"
]

print("\nTest Predictions\n")

# Predict category
for query in test_queries:

    prediction = model.predict(
        vectorizer.transform([query])
    )[0]

    print(f"{query}")
    print(f"Prediction: {prediction}\n")

# Save model
joblib.dump(model, "query_classifier.pkl")

# Save vectorizer
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved successfully")