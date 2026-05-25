from flask import Flask, request, send_file, render_template
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_google_results(keyword):
    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": keyword,
        "api_key": os.getenv("SERPAPI_KEY")
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for item in data.get("organic_results", []):
        results.append({
            "position": item.get("position"),
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet")
        })

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        keyword = request.form["keyword"]
        results = get_google_results(keyword)

        with open(
            "results.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                results,
                file,
                ensure_ascii=False,
                indent=2
            )

    return render_template(
        "index.html",
        results=results
    )


@app.route("/download")
def download():
    return send_file("results.json", as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
