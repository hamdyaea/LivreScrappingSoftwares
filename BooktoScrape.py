from fonctions import *
from tqdm import tqdm
import time

# Début du chrono
start_time = time.time()

# Adresse du site à analyser
url_general = "https://books.toscrape.com/catalogue/page-1.html"

# Définir l'ordre des colonnes CSV
liste_entete = [
    "title", "category", "image", "url", "upc", "tax", "no_tax",
    "availability", "description", "review"
]

# Définir la valeur des entêtes CSV
dico_entete = {
    "url": "Product_page_url",
    "upc": "Universal_product_code (upc)",
    "title": "Title",
    "tax": "Price_including_tax",
    "no_tax": "Price_excluding_tax",
    "availability": "Number_available",
    "description": "Product_description",
    "category": "Category",
    "review": "Review_rating",
    "image": "Image_url"
}

# Définir le nom du fichier csv
nom_du_csv = "export_livre"

# Définir le nom du fichier csv image
fichier_image = "image"

# Initialisation du fichier csv
creation_csv(liste_entete, dico_entete, nom_du_csv)

# Récupération de la liste des liens d'ouvrage
print("Calcul du nombre d'ouvrage sur le site :")
liste_ouvrage_categorie = []
lancement_export_ouvrage(url_general, liste_ouvrage_categorie)

print("Il y a", len(liste_ouvrage_categorie), "ouvrages sur le site")

for livre in tqdm(liste_ouvrage_categorie, desc="Analyse en cours", unit="livre"):
    url_courant_livre = livre
    analyse_livre(liste_entete, dico_entete, url_general, url_courant_livre, nom_du_csv, fichier_image)

print("Fin de l'analyse", "\nAnalyse réalisée en", int(time.time() - start_time), "secondes")

