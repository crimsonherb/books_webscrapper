from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

from django.core.paginator import Paginator

# Create your views here.
def get_html_content(page):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    html_content = session.get(f"http://books.toscrape.com/catalogue/page-{page}.html").text
    status = session.get(f"http://books.toscrape.com/catalogue/page-{page}.html").status_code

    soup = BeautifulSoup(html_content, 'lxml')

    return [soup, status]

def get_html_links(soup):
    links = []
    listings = soup.find_all(attrs={"class":"product_pod"})
    for listing in listings:
        book_link = listing.find("h3").a.get("href")
        base_url = "http://books.toscrape.com/catalogue/"
        complete_url = base_url +  book_link
        links.append(complete_url)
    return links

def get_info(links):
    result = []
    for link in links:
        req = requests.get(link).text
        book_soup = BeautifulSoup(req,'lxml')

        title = book_soup.find(attrs={'class':'product_main'}).h1.text.strip()
        price = book_soup.find(attrs={'class':'product_main'}).p.text.strip()[2:]
        # stock = book_soup.find(attrs={'class':'product_main'}).text.strip()

        # book = {"title":title, "price":price, "stock":stock}
        book = {"title":title, "price":price}
        result.append(book)
    return result

def base(request):
    
    result_books = []
    page = 1
    while True:

        html_data = get_html_content(page)
        if html_data[1] == 200:
            print(f" scrapping page {page} ")
            all_links = get_html_links(html_data[0])
            result = get_info(all_links)
            result_books.append(result)
            page += 1
        else:
            print("The End")
            break

        
    # p = Paginator(result_books,2)
    # page = request.GET.get('page')
    # venues = p.get_page(page)
    print(result_books)
    return render(request, 'core/index.html',{'result': result_books})

