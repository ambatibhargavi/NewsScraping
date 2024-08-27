from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


# Function to scrape headlines from a given URL
def scrape_headlines(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = []

        # Common headline tags to check
        tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        for tag in tags:
            for item in soup.find_all(tag):
                headlines.append(item.get_text(strip=True))

        # Remove duplicates and empty headlines
        headlines = list(set([h for h in headlines if h]))

        return headlines
    except Exception as e:
        return [f"Error: {str(e)}"]


# Route to display the form and results
@app.route('/', methods=['GET', 'POST'])
def index():
    headlines_html = ""
    if request.method == 'POST':
        url = request.form.get('url')

        if url:
            headlines = scrape_headlines(url)
            headlines_html = "<h2>Scraped Headlines:</h2>"
            for headline in headlines:
                headlines_html += f"<p>- {headline}</p>"
        else:
            headlines_html = "<p>Please enter a URL.</p>"

    return render_template_string("""
    <!doctype html>
    <html>
    <head><title>News Scraper</title></head>
    <body>
        <h1>News Scraper</h1>
        <form method="post">
            <label for="url">Enter URL:</label><br>
            <input type="text" id="url" name="url" required><br><br>
            <input type="submit" value="Scrape">
        </form>
        {{ headlines_html|safe }}
    </body>
    </html>
    """, headlines_html=headlines_html)


if __name__ == "__main__":
    app.run(port=5001)
