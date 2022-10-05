from unittest import result
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
# Create your views here.
def get_html_content(page):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    html_content = session.get(f"http://books.toscrape.com/catalogue/page-{page}.html").text

    return html_content

def base(request):
    page = 1
    html_content = get_html_content(1)
    soup = BeautifulSoup(html_content, 'html.parser')
    result = dict()
    result['title']
    print(result['title'])

    return render(request, 'core/base.html')

