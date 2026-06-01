# Tamil NLP Detector — தமிழ் உரை பகுப்பாய்வி

> Sentiment Analysis & Fake News Detection for Tamil Language

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://tamil-nlp-sentiment-and-fake-news-detector.streamlit.app/)
[![Kaggle Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle)](https://www.kaggle.com/datasets/muthumarii/tamil-nlp-sentiment-and-fake-news-dataset)
[![Hugging Face](https://img.shields.io/badge/Dataset-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/datasets/Muthumari10/tamil-nlp-sentiment-and-fake-news-dataset)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python)](https://python.org)

---

## 📌 Project Overview

Tamil NLP Detector is a text classification web application that analyzes Tamil language text and classifies it into one of four categories:

| Label | Description |
|-------|-------------|
| ✅ **Positive** | Happy, appreciative, or achievement-oriented sentiment |
| ❌ **Negative** | Sad, frustrated, complaint, or loss-related sentiment |
| ⚠️ **Fake** | Misinformation, WhatsApp scams, false health claims |
| 📰 **Real** | Verified news, government announcements, factual reporting |

This project addresses a real-world problem — Tamil is a low-resource language with very few publicly available NLP datasets. This project creates, publishes, and models on an **original Tamil dataset** covering both formal (செய்தி மொழி) and colloquial (பேச்சு வழக்கு) Tamil.

---

## 🚀 Live Demo

👉 **[https://tamil-nlp-sentiment-and-fake-news-detector.streamlit.app/](https://tamil-nlp-sentiment-and-fake-news-detector.streamlit.app/)**

---

## 🗃️ Dataset

- **820 rows** — 205 per label (perfectly balanced)
- **4 labels** — positive, negative, fake, real
- **0 duplicates** — verified with deduplication
- **Encoding** — UTF-8-SIG (Tamil script renders correctly in Excel)
- **Splits** — train (80%) / validation (10%) / test (10%) with seed 42
- **Domains covered:**
  - Positive: relationships, achievements, food, travel, nature, festivals
  - Negative: service complaints, personal failure, social issues, mental state
  - Fake: health cures, WhatsApp forwards, astrology threats, fake schemes
  - Real: politics, sports, court orders, weather, infrastructure, economy

📦 Dataset published on:
- [Kaggle](https://www.kaggle.com/datasets/muthumarii/tamil-nlp-sentiment-and-fake-news-dataset)
- [Hugging Face](https://huggingface.co/datasets/Muthumari10/tamil-nlp-sentiment-and-fake-news-dataset)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10 |
| ML Model | Scikit-learn — Logistic Regression |
| Feature Extraction | TF-IDF (char n-grams, 2–4) |
| Web Framework | Streamlit |
| Model Persistence | Joblib |
| Dataset Format | CSV (UTF-8-SIG) |
| Deployment | Streamlit Cloud |
| Dataset Hosting | Kaggle, Hugging Face |

---

## 📁 Project Structure

```
tamil_nlp_detector/
│
├── app.py                  # Streamlit web application
├── train_model.py          # Model training script
├── tamil_nlp_model.pkl     # Trained model (generated after training)
│
├── tamil_nlp_full.csv      # Full dataset (820 rows)
├── train.csv               # Training split (656 rows, 80%)
├── validation.csv          # Validation split (82 rows, 10%)
├── test.csv                # Test split (82 rows, 10%)
│
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Muthumari10/tamil_nlp_detector.git
cd tamil_nlp_detector
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python train_model.py
```
This generates `tamil_nlp_model.pkl` and prints accuracy scores.

### 4. Run the app
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Validation Accuracy | ~88–92% |
| Model Type | Logistic Regression |
| Feature Extractor | TF-IDF (char 2–4 grams) |
| Training Rows | 656 |
| Test Rows | 82 |

> Character-level n-gram TF-IDF works well for Tamil because it captures morphological patterns without requiring a Tamil tokenizer.

---

## 📋 Requirements

```
streamlit
scikit-learn
pandas
joblib
```

Install with:
```bash
pip install streamlit scikit-learn pandas joblib
```

---

## 🌐 Features

- 🔎 Real-time Tamil text classification
- 📊 Confidence breakdown across all 4 labels
- ⚡ 8 one-click example sentences
- 🕐 Recent analysis history panel
- ⚠️ Non-Tamil input detection with bilingual error message
- 🎨 Fully responsive dark UI with Tamil cultural design
- 📱 Works on desktop and mobile

---

## 🔮 Future Improvements

- [ ] Fine-tune IndicBERT for higher accuracy
- [ ] Expand dataset to 5000+ rows
- [ ] Add Tamil speech-to-text input
- [ ] Include regional dialect coverage (Madurai, Coimbatore, Tirunelveli)
- [ ] Connect to live Tamil news API for real-time verification
- [ ] Add user feedback loop to improve model over time

---

## 👩‍💻 Author

**Sudalaimuthumari M**
B.Tech — Artificial Intelligence & Data Science

[![GitHub](https://img.shields.io/badge/GitHub-Muthumari10-181717?style=flat&logo=github)](https://github.com/Muthumari10)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/sudalaimuthumarim)
[![Kaggle](https://img.shields.io/badge/Kaggle-muthumarii-20BEFF?style=flat&logo=kaggle)](https://www.kaggle.com/muthumarii)

---

## 📄 License

Dataset licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code is open source — feel free to use and build upon this project.

---

<div align="center">
  <sub>Built with ❤️ for Tamil language NLP · தமிழ் · அறிவியல் · தொழில்நுட்பம்</sub>
</div>
