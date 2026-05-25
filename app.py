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
    print(data)

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
    if request.method == "POST":
        keyword = request.form["keyword"]
        results = get_google_results(keyword)

        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=2)

        html = "<h1>Results</h1>"
        html += '<a href="/download">Download JSON</a><br><br>'

        for result in results:
            html += f"<h3>{result['position']}. {result['title']}</h3>"
            html += f"<a href='{result['url']}'>{result['url']}</a>"
            html += f"<p>{result['snippet']}</p>"

        return html

    return """
    <h1>Google Organic Results</h1>
    <form method="POST">
        <input name="keyword" placeholder="Enter keyword phrase">
        <button type="submit">Search</button>
    </form>
    """


@app.route("/download")
def download():
    return send_file("results.json", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)