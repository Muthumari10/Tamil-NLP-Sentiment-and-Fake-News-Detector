import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load data
train_df = pd.read_csv('train.csv')
val_df   = pd.read_csv('validation.csv')
test_df  = pd.read_csv('test.csv')

print(f"Train size: {len(train_df)}")
print(f"Val size:   {len(val_df)}")
print(f"Test size:  {len(test_df)}")
print(f"Labels:     {train_df['label'].unique()}")

# Build pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        analyzer='char',
        ngram_range=(2, 4),
        max_features=50000,
        sublinear_tf=True
    )),
    ('clf', LogisticRegression(
        max_iter=1000,
        C=5,
        class_weight='balanced'
    ))
])

# Train
pipeline.fit(train_df['text'], train_df['label'])

# Evaluate on validation
val_preds = pipeline.predict(val_df['text'])
print("\n--- Validation Results ---")
print(f"Accuracy: {accuracy_score(val_df['label'], val_preds):.2%}")
print(classification_report(val_df['label'], val_preds))

# Evaluate on test
test_preds = pipeline.predict(test_df['text'])
print("--- Test Results ---")
print(f"Accuracy: {accuracy_score(test_df['label'], test_preds):.2%}")
print(classification_report(test_df['label'], test_preds))

# Save model
joblib.dump(pipeline, 'tamil_nlp_model.pkl')
print("\nModel saved as tamil_nlp_model.pkl")