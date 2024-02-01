import requests
import re
from flask import Flask, jsonify

app = Flask(__name__)

def get_latest_stories():
    """
    Fetches the latest stories from the 'https://time.com/' website.

    Returns:
        list: A list of dictionaries containing the cleaned titles and links of the latest stories.
    """
    url = "https://time.com/"
    response = requests.get(url)
    result = []

    if response.status_code == 200:
        html_content = response.text
        latest_stories_start = html_content.find(
            '<ul class="featured-voices__list swipe-h">'
        )
        latest_stories_end = html_content.find("</ul>", latest_stories_start)

        latest_stories_section = html_content[latest_stories_start:latest_stories_end]
        titles = re.findall(
            r'<h3 class="featured-voices__list-item-headline display-block">(.*?)</h3>',
            latest_stories_section,
            re.DOTALL,
        )
        links = re.findall(r'<a href="([^"]+)">', latest_stories_section)
        assert 2 * len(titles) == len(links)
        links = [link for i, link in enumerate(links) if i % 2 == 1]
        for title, link in zip(titles, links):
            cleaned_title = " ".join(title.split())
            cleaned_link = " ".join(link.split())
            result.append({
                "Title": cleaned_title,
                "Link": f"{url}{cleaned_link}"
            })
        return result
    else:
        print(f"Failed to fetch news. Status code: {response.status_code}")

@app.route('/api/latest_stories')
def api_latest_stories():
    """
    Flask route to expose the latest stories as a JSON API.

    Returns:
        Flask Response: JSON response containing the latest stories.
    """
    latest_stories = get_latest_stories()
    return jsonify(latest_stories)

if __name__ == '__main__':
    app.run(debug=True)
