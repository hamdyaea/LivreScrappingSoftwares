import requests
import re
import os
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def lancement_export_ouvrage(url_general, liste_ouvrage_categorie):
    soup_actuel = export_ouvrage(url_general, liste_ouvrage_categorie)

    while soup_actuel.find("ul", class_="pager"):
        soup_provisoire = soup_actuel.find("ul", class_="pager")
        if soup_provisoire.find("li", class_="next"):
            soup_provisoire = soup_provisoire.find("li", class_="next").find_next()
            url_provisoire = soup_provisoire["href"]
            url_actuel_categorie = urljoin(str(url_general), str(url_provisoire))
            soup_actuel = export_ouvrage(url_actuel_categorie, liste_ouvrage_categorie)
        else:
            break


def export_ouvrage(url_general, liste_ouvrage_categorie):
    page_actuel = requests.get(url_general)
    soup_actuel = BeautifulSoup(page_actuel.content, "html.parser")

    for balise in soup_actuel.find_all("a"):
        if balise.get("title"):
            url_provisoire = balise["href"]
            balise_url = urljoin(str(url_general), str(url_provisoire))
            liste_ouvrage_categorie.append(balise_url)

    return soup_actuel


def creation_csv(liste_entete, dico_entete, nom_du_csv):
    liste_entete_csv_export = []

    for key in liste_entete:
        liste_entete_csv_export.append(dico_entete[key])

    with open(nom_du_csv + ".csv", "w", newline="", encoding="utf-32") as fichiercsv:
        writer = csv.writer(fichiercsv, delimiter=",")
        writer.writerow(liste_entete_csv_export)


def analyse_livre(liste_entete, dico_entete, url_general, url_courant_livre, nom_du_csv, fichier_image):
    page = requests.get(url_courant_livre)
    soup = BeautifulSoup(page.content, "html.parser")
    dico_courant = {}

    dico_courant["url"] = url_courant_livre

    balise_title = soup.find("div", class_="col-sm-6 product_main").find("h1")
    dico_courant["title"] = "\"" + balise_title.get_text() + "\""

    balise_description = soup.find("div", id="product_description")
    if balise_description:
        balise_description = balise_description.find_next("p")
        dico_courant["description"] = "\"" + balise_description.get_text() + "\""
    else:
        dico_courant["description"] = "Pas de description pour cet ouvrage"

    balise_category = soup.find("ul", class_="breadcrumb")
    for balise in balise_category:
        if balise.get_text() == balise_title.get_text():
            balise_category = balise.find_previous_sibling()
            dico_courant["category"] = balise_category.get_text()[1:-1]

    balises_th = soup.find_all("th")
    for balise in balises_th:
        if balise.get_text() == "UPC":
            dico_courant["upc"] = balise.find_next().get_text()
        elif balise.get_text() == "Price (excl. tax)":
            dico_courant["no_tax"] = balise.find_next().get_text()
        elif balise.get_text() == "Price (incl. tax)":
            dico_courant["tax"] = balise.find_next().get_text()
        elif balise.get_text() == "Availability":
            availability_balise = balise.find_next().get_text()
            dico_courant["availability"] = re.findall("\d+", availability_balise)[0]
        elif balise.get_text() == "Number of reviews":
            dico_courant["review"] = balise.find_next().get_text()

    for image in soup.findAll("img"):
        if image.get('alt', '') == balise_title.get_text():
            balise_url_provisoire = image['src']

    balise_url = urljoin(str(url_general), str(balise_url_provisoire))
    dico_courant["image"] = balise_url

    if not os.path.exists(fichier_image + "/" + dico_courant["category"]):
        os.makedirs(fichier_image + "/" + dico_courant["category"])

    nom_livre = re.split('/', url_courant_livre)
    adresse_image = fichier_image + "/" + dico_courant["category"] + "/" + nom_livre[-2] + ".jpg"

    if not os.path.exists(adresse_image):
        with open(adresse_image, 'wb') as f:
            response = requests.get(balise_url)
            f.write(response.content)

    liste_ouvrage_csv_export = []

    for key in liste_entete:
        liste_ouvrage_csv_export.append(dico_courant[key])

    with open(nom_du_csv + ".csv", "a", newline="", encoding="utf-32") as fichiercsv:
        writer = csv.writer(fichiercsv, delimiter=",")
        writer.writerow(liste_ouvrage_csv_export)
