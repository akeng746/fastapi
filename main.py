from fastapi import FastAPI
import openai
import requests

#imports and stuff for Fast API
import os
from dotenv import load_dotenv
load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')

app = FastAPI()

# API Keys
NEWS_API_KEY = "343be45b17d94c69bbf06c9fb38159e3"

openai.api_key = os.getenv('OPENAI_KEY')

# Fetch News Articles
def get_news():
    url = f"https://newsapi.org/v2/everything?q=ICE+arrests&language=en&sortBy=publishedAt&pageSize=6&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    return news_data.get("articles", [])

# Summarize News Articles using OpenAI
def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Summarize this news article in 3 bullet points:\n" + text}],
        max_tokens=150
    )
    return response.choices[0].message["content"]

# FastAPI Endpoint to Get Summarized News
@app.get("/news")
async def get_summarized_news():
    articles = get_news()
    summarized_articles = []

    for article in articles:
        title = article.get("title", "No title")
        description = article.get("description", "No description available.")
        summary = summarize_text(title + ". " + description)

        summarized_articles.append({
            "title": title,
            "summary": summary
        })

    return {"articles": summarized_articles}

