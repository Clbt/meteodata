import requests
from bs4 import BeautifulSoup
import os

# URL de la page avec les fichiers
page_url = "https://explore.data.gouv.fr/fr/datasets/6569b4473bedf2e7abad3b72/#/resources/16bd3e0e-33dd-4389-83a9-dd26114f84f7"

# Fonction pour télécharger un fichier
def download_file(url, folder_path):
    local_filename = url.split('/')[-1]
    file_path = os.path.join(folder_path, local_filename)

    # Envoyer la requête pour télécharger le fichier
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Fichier téléchargé : {local_filename}")
    return file_path

# Télécharger la page web
response = requests.get(page_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Créer un dossier pour les fichiers téléchargés
download_folder = "fichiers_telecharges"
os.makedirs(download_folder, exist_ok=True)

# Trouver tous les liens vers les fichiers
file_links = soup.find_all('a', href=True)

# Filtrer les liens vers les fichiers spécifiques
file_urls = [link['href'] for link in file_links if "datasets" in link['href']]

# Télécharger chaque fichier
for file_url in file_urls:
    full_url = f"https://explore.data.gouv.fr{file_url}"  # Construire l'URL complète
    download_file(full_url, download_folder)

