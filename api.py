from flask import Flask, request, jsonify
import subprocess
from utils import fetch_news_links, summarize_text, analyze_sentiment, extract_topics, generate_hindi_tts

app = Flask(__name__)

@app.route('/news', methods=['GET'])
def get_news():
    """Fetches news articles and generates TTS."""
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = fetch_news_links(company)
    if not articles:
        return jsonify({"error": "No news articles found for this company."}), 404

    processed_articles = [
        {
            "Title": article["Title"],
            "Summary": summarize_text(article["Content"]),
            "Sentiment": analyze_sentiment(article["Content"]),
            "Topics": extract_topics(article["Content"]),
            "URL": article["URL"]
        }
        for article in articles
    ]

    summary_text = " ".join([a["Summary"] for a in processed_articles])
    audio_filename = generate_hindi_tts(summary_text, company)

    return jsonify({
        "Company": company,
        "Articles": processed_articles,
        "Final Sentiment Analysis": "Overall sentiment is positive." if any(a["Sentiment"] == "Positive" for a in processed_articles) else "Overall sentiment is neutral or negative.",
        "AudioFile": audio_filename,
        "Status": "Processing Complete!"
    })

if __name__ == '__main__':
    print(" API Running on http://127.0.0.1:5000")
    subprocess.Popen(["python", "app.py"])  # Start UI automatically
    app.run(debug=True, use_reloader=False)
