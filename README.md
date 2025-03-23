# 📰 News Summarization and Text-to-Speech (TTS) Application

## 📌 Project Overview
This project is a web-based application that extracts key details from multiple news articles related to a given company, performs **sentiment analysis**, conducts **comparative analysis**, and generates a **text-to-speech (TTS) output in Hindi**.

### 🚀 Features:
- **News Extraction**: Fetches at least 10 articles using `NewsAPI` and scrapes content via `BeautifulSoup`.
- **Sentiment Analysis**: Classifies article content as **Positive, Negative, or Neutral**.
- **Comparative Analysis**: Compares sentiment trends across different articles.
- **Hindi Text-to-Speech (TTS)**: Converts summarized content into Hindi speech.
- **User Interface**: Interactive UI using `Gradio` for easy access.
- **API Development**: Backend `Flask API` to fetch, analyze, and process data.
- **Deployment**: Deployable on **Hugging Face Spaces**.

---

## 📂 Project Structure
```
NewsSummarizationTTS/
│── venv/                # Virtual environment
│── app.py               # Web interface using Gradio
│── api.py               # Backend Flask API
│── utils.py             # Core functions (scraping, summarization, sentiment analysis, TTS)
│── config.py            # Configuration settings (API keys, constants)
│── requirements.txt     # Required dependencies
│── README.md            # Project documentation
│── static/              # Stores generated TTS audio files
│── logs/                # Log files for debugging
│── __pycache__/         # Compiled Python files (ignored in Git)
```

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mahin78692/NewsSummarizationTTS.git
cd NewsSummarizationTTS
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up API Keys (NewsAPI)
Create a `.env` file and add:
```env
NEWS_API_KEY=your_api_key_here
```

### 5️⃣ Run the Application
Start the backend API:
```bash
python api.py
```
Run the frontend UI:
```bash
python app.py
```

---

## 🎯 Usage Guide
1. Enter the **company name** in the UI.
2. The app fetches and **summarizes** relevant news articles.
3. It performs **sentiment analysis** & generates a **comparative report**.
4. Hindi **text-to-speech (TTS)** is generated for easy listening.
5. Download the **.mp3 audio file** of the news summary.

---

## 🔥 Technologies Used
- **Python** (Flask, BeautifulSoup, NLTK, Transformers)
- **Gradio** (for UI)
- **gTTS** (for Hindi TTS conversion)
- **KeyBERT** (for topic extraction)
- **NewsAPI** (for fetching articles)
- **Hugging Face Transformers** (for summarization)

---

## 📊 Model Analysis
Project utilizes several **pretrained NLP models and libraries** for different functionalities. Below is a breakdown of each:

### 1️⃣ Summarization Model  
📌 **Model Used:** `sshleifer/distilbart-cnn-12-6` (Hugging Face Transformers)  
🔹 **Description:**  
- A **DistilBART** model fine-tuned on the **CNN/DailyMail** dataset.
- Generates **abstractive summaries** of long articles.
- **Implementation in `utils.py`:**
```python
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
```

---

### 2️⃣ Sentiment Analysis Model  
📌 **Model Used:** `VADER` (Valence Aware Dictionary and sEntiment Reasoner) from `NLTK`  
🔹 **Description:**  
- A **lexicon-based** sentiment analysis tool.
- Classifies text into **Positive, Negative, or Neutral** based on sentiment scores.
- **Implementation in `utils.py`:**
```python
sia = SentimentIntensityAnalyzer()
score = sia.polarity_scores(text)
```

---

### 3️⃣ Topic Extraction Model  
📌 **Model Used:** `KeyBERT` (Keyword Extraction with BERT)  
🔹 **Description:**  
- Extracts **key topics** from text using a **BERT-based embedding model**.
- Helps identify **main themes** of a news article.
- **Implementation in `utils.py`:**
```python
kw_model = KeyBERT()
topics = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
```

---

### 4️⃣ Hindi Text-to-Speech (TTS) Model  
📌 **Model Used:** `Google Text-to-Speech (gTTS)`  
🔹 **Description:**  
- Converts **English** or **translated Hindi text** into natural Hindi speech.
- Uses **Google's TTS API** for text-to-speech conversion.
- **Implementation in `utils.py`:**
```python
tts = gTTS(text=translated_text, lang='hi')
tts.save(filename)
```

---
