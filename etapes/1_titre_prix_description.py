import requests
from bs4 import BeautifulSoup

# URL de la page d'un livre
url_livre = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Obtenir le contenu de la page
response = requests.get(url_livre)
html = response.content

# Analyser le code HTML avec Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Récupérer le titre du livre
title = soup.find('h1').text
print(title)

# Récupérer le prix du livre
price = soup.find('p', class_='price_color').text
print(price)

# Récupérer la description du livre
description = soup.find('div', id='product_description').next_sibling.next_sibling.text.strip()
print(description)
