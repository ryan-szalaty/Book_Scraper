import requests
import sqlite3
from bs4 import BeautifulSoup

response = requests.get("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article")
    
    
def get_title(book):
    title = book.find("h3").find("a")["title"]
    return title
    
def get_price(book):
    price = float((book.select(".price_color")[0].get_text()[2::]))
    return price
    
def get_rating(book):
    ratings = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = book.select(".star-rating")[0].get_attribute_list("class")[-1]
    converted_rating = ratings[rating]
    return converted_rating
    

def scrape_books():
    all_books = []
    for book in books:
        book_data = (get_title(book), get_price(book), get_rating(book))
        all_books.append(book_data)
    save_books(all_books)
    return all_books #returns tuple with list of books
    
def save_books(all_books):
    connection = sqlite3.connect("scraped_books.db")
    c = connection.cursor()
    
    #c.execute("CREATE TABLE books (title TEXT, price REAL, rating INTEGER)")
    
    c.executemany("INSERT INTO books VALUES (?,?,?)", all_books)
    
    connection.commit()
    connection.close()
    
scrape_books()