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
                'description': description[:1000] + "..." if len(description) > 200 else description
            }
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None


def search_goodreads_books(query):
    search_url = f"https://www.goodreads.com/search?q={query.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            book_elements = soup.find_all('a', {'class': 'bookTitle'})
            for book in book_elements[:5]: 
                book_title = book.text.strip()
                book_author = book.find_next_sibling('span', {'itemprop': 'author'}).text.strip()
                book_link = "https://www.goodreads.com" + book['href']
                results.append({'title': book_title, 'author': book_author, 'link': book_link})
            return results
        else:
            print(f"Failed to fetch search results. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


query = input("Enter book title or author to search: ")
search_results = search_goodreads_books(query)
if search_results:
    print("Search Results:")
    for idx, book in enumerate(search_results):
        print(f"{idx + 1}. {book['title']} - {book['author']}")
    
    choice = int(input("Select a book by number to get details: ")) - 1
    if 0 <= choice < len(search_results):
        book_url = search_results[choice]['link']
    else:
        print("Invalid choice.")
        exit()
book_info = scrape_goodreads_book(book_url)

print("=================================================================")
if book_info:
    print("Book Information:")
    print(f"Title: {book_info['title']}")
    print(f"Author: {book_info['author']}")
    print(f"Rating: {book_info['rating']}")
    print(f"Description: {book_info['description']}")