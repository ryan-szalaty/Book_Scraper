import requests
import csv
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader

base_url = "https://quotes.toscrape.com"

def read_quotes(filename):
    with open(filename, "r", encoding = "utf-8") as file:
        csv_reader = DictReader(file)
        quotes = list(csv_reader)
        return quotes

def play_again():
    answer = input("Would you like to play again? Please input Yes or No: ")
    if answer.lower() in ("y", "yes"):
        play_game(quotes)
    else:
        print("Thank you for playing!")
        exit()

def play_game(quotes):  
    quote = choice(quotes)
    remaining_guesses = 4
    print(f"Here's a quote: {quote['text']}")

    guess = ""

    while guess.lower() != quote["author"].lower():
        guess = input(f"Who said this? Remaining guesses: {remaining_guesses}.\n")
        if guess.lower() == quote["author"].lower():
            print("You are correct!")
            play_again()
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{base_url + quote['link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            hint_date = soup.find(class_ = "author-born-date").get_text()
            hint_location = soup.find(class_ = "author-born-location").get_text()
            print(f"Hint: This author was born on {hint_date + ' ' + hint_location}")
        elif remaining_guesses == 2:
            print(f"Hint: The first initial is {quote['author'][0]}")
        elif remaining_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(f"Hint: The last initial is {last_initial}")
        else:
            print(f"Answer: {quote['author']}.")
            play_again()

def write_quotes(quotes):
    with open("quotes.csv", "w") as file:
        headers = ["text", "author", "link"]
        csv_writer = DictWriter(file, fieldnames = headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = read_quotes("quotes.csv")
play_game(quotes)