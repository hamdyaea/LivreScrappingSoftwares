import os
import requests
from bs4 import BeautifulSoup

# Création du dossier images s'il n'existe pas déjà
if not os.path.exists("images"):
    os.makedirs("images")

# Récupération de la liste de toutes les catégories
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
categories = soup.select("ul.nav-list > li > ul > li > a")

# Parcours de toutes les catégories
for category in categories:
    category_url = url + category["href"]
    category_name = category.text.strip().lower()

    # Création du sous-dossier de la catégorie s'il n'existe pas déjà
    if not os.path.exists(f"images/{category_name}"):
        os.makedirs(f"images/{category_name}")

    # Récupération de la liste de tous les livres de la catégorie
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.select("article.product_pod")

    # Parcours de tous les livres de la catégorie
    for article in articles:
        # Récupération de l'URL de l'image du livre
        image_url = url + article.select_one("img")["src"].replace("../", "")

        # Téléchargement de l'image et enregistrement dans le dossier de la catégorie correspondante
        response = requests.get(image_url)
        with open(f"images/{category_name}/{article.select_one('h3 > a')['href'].split('/')[-2]}.jpg", "wb") as f:
            f.write(response.content)
