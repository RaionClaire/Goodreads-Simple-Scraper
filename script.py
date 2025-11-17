import requests
from bs4 import BeautifulSoup
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_goodreads_book(book_url):
    try:
        response = requests.get(book_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_element = soup.find('h1', {'data-testid': 'bookTitle'})
            title = title_element.text.strip() if title_element else "Title not found"
            
            author_element = soup.find('span', {'data-testid': 'name'})
            author = author_element.text.strip() if author_element else "Author not found"
            
            rating_element = soup.find('div', {'class': 'RatingStatistics__rating'})
            rating = rating_element.text.strip() if rating_element else "Rating not found"
            
            description_element = soup.find('div', {'class': 'DetailsLayoutRightParagraph__widthConstrained'})
            description = description_element.text.strip() if description_element else "Description not found"
            
            return {
                'title': title,
                'author': author,
                'rating': rating,
                'description': description[:200] + "..." if len(description) > 200 else description
            }
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

book_url = "https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird"
book_info = scrape_goodreads_book(book_url)

if book_info:
    print("Book Information:")
    print(f"Title: {book_info['title']}")
    print(f"Author: {book_info['author']}")
    print(f"Rating: {book_info['rating']}")
    print(f"Description: {book_info['description']}")