import requests
from bs4 import BeautifulSoup
import json

url = 'http://books.toscrape.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Обойти все страницы каталога и собрать ссылки на книги, пройти по ссылкам и собрать информацию о книгах

# Список всех книг

books = []
books_links = []

# Собираем ссылки на книги

for i in range(1, 3):
    response = requests.get(url + f'catalogue/page-{i}.html')
    soup = BeautifulSoup(response.text, 'html.parser')
    for book in soup.find_all('h3'):
        books_links.append(url + 'catalogue/' + book.a.get('href'))

# Собираем информацию о книгах

for link in books_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.h1.text
    price = soup.find('p', class_='price_color').text
    availability = soup.find('p', class_='instock availability').text.strip()
    availability_to_int = int(availability.split()[2].replace('(', '').replace(')', '').split()[0]) 
    books.append({
        'title': title,
        'price': price,
        'availability': availability_to_int,
    })

# Сохраняем информацию о книгах в файл json

with open('books.json', 'w') as file:
    json.dump(books, file, indent=2)


