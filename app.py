import gradio as gr
import requests

API_URL = "http://127.0.0.1:5000/news"

def fetch_news(company):
    response = requests.get(API_URL, params={"company": company})
    if response.status_code != 200:
        return "Error fetching data."
    
    data = response.json()
    return f"🔹 **Company:** {data['Company']}\n🔹 **Articles Found:** {len(data['Articles'])}\n🔹 **Sentiment Analysis:** {data['Final Sentiment Analysis']}\n🔹 **Listen:** [Download Hindi Speech]({data['AudioFile']})"

iface = gr.Interface(fn=fetch_news, inputs="text", outputs="text", title="News Summarization & TTS")
iface.launch()
