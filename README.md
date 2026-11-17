# 🛡️ SpamShield — Email Spam Detection

**SpamShield** is an AI-powered email spam detection application built using Machine Learning. It classifies emails as **Spam** or **Ham (Legitimate)** using Natural Language Processing and Logistic Regression.

The application accepts both manually entered email content and `.eml` email files, making it possible to analyze real email messages through a simple web interface.

🔗 **Live Demo:** https://spamshield-6kyxdxdcuhuha9mnw7gbaz.streamlit.app/

---

## 🚀 Features

- **Email Classification:** Predicts whether an email is Spam or Ham.
- **Email File Upload:** Supports `.eml` files.
- **MIME Parsing:** Extracts email subjects and bodies from MIME-formatted messages.
- **HTML Processing:** Extracts readable text from HTML email bodies.
- **URL Normalization:** Replaces URLs with a common `URL` token.
- **TF-IDF Vectorization:** Converts email text into numerical features.
- **Probability-Based Classification:** Uses a tuned classification threshold.
- **Interactive Interface:** Built using Streamlit.

## 🧰 Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF |
| Model | Logistic Regression |
| Email Parsing | Python Email Package |
| HTML Parsing | BeautifulSoup |
| Model Persistence | Joblib |
| Web Application | Streamlit |

## 📂 Dataset

The project uses the **Apache SpamAssassin Public Corpus**, containing legitimate and spam email messages.

The dataset was organized into two categories:

- Ham: 2,500 emails
- Spam: 502 emails
- Total: 3,002 emails

A stratified train-test split was performed:

- Training set: 80%
- Testing set: 20%

The test set was kept separate during model development and used for final evaluation.

*Note: The raw email dataset is not included in this repository.*

## ⚙️ Project Workflow

### 1. Exploratory Data Analysis

Performed EDA to understand:

- Distribution of Ham and Spam emails.
- Email file sizes and body lengths.
- HTML content and MIME structures.
- Multipart email patterns.
- Attachment frequency.

### 2. Email Preprocessing

Created a custom preprocessing pipeline to handle email messages.

The pipeline:

1. Reads raw email files.
2. Parses MIME-formatted messages.
3. Extracts the subject and email body.
4. Prefers plain-text content, with HTML as a fallback.
5. Extracts readable text from HTML using BeautifulSoup.
6. Normalizes URLs and numerical sequences.
7. Removes unnecessary whitespace.

### 3. Feature Extraction

Used **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert email text into numerical feature vectors.

The fitted vectorizer is included within the final machine learning pipeline.

### 4. Model Training

Experimented with:

- Multinomial Naive Bayes
- Logistic Regression

Logistic Regression with `class_weight="balanced"` achieved substantially better performance on this dataset.

### 5. Threshold Optimization

Instead of relying only on the default classification threshold of 0.5, the threshold was selected using out-of-fold predictions from cross-validation.

The selected threshold was approximately **0.3981**, based on the best F1-score.

This threshold was then used for final test-set evaluation.

## 📊 Model Performance

The final Logistic Regression pipeline was evaluated on the held-out test set.

| Metric | Test Score |
|---|---:|
| Precision | 0.95 |
| Recall | 0.96 |
| F1-Score | 0.96 |
| Average Precision | 0.92 |
| ROC-AUC | 0.98 |

These results indicate strong classification performance on the held-out dataset.

## 🏗️ Project Structure

```text
spam-classifier/
│
├── .streamlit/
│   └── config.toml
│
├── notebooks/
│   └── spam_classification.ipynb
│
├── app.py
├── model.py
├── preprocessing.py
│
├── spam_classifier.pkl
├── spam_threshold.pkl
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/spamshield.git
```

### 2. Navigate to the project directory

```bash
cd spamshield
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open locally in your browser.

## ⚠️ Limitations

- The classifier relies primarily on extracted subject and body text.
- MIME metadata, attachment contents and attachment types are not directly used as independent model features.
- The model's probability is an estimate, not a guarantee that an email is malicious or legitimate.
- The model may encounter email formats and writing patterns that differ from its training dataset.

**SpamShield is an educational machine learning project, not a replacement for dedicated email security software.**

## 🎯 Future Improvements

- Incorporate structured MIME and attachment metadata.
- Experiment with additional NLP features.
- Evaluate the model on newer and more diverse email datasets.
- Improve probability calibration and generalization.

---

**Built with Python, Scikit-learn and Streamlit.**
