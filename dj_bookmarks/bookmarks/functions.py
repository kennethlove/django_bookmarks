import requests


def fetch_url_title(url):
    try:
        r = requests.get(url, timeout=2)
    except requests.exceptions.ConnectionError:
        return

    if r.ok:
        text = r.text
        title = text[text.find('<title>') + 7:text.find('</title>')]
        return title
