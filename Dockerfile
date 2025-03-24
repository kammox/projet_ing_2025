# Utiliser une image Python légère
FROM python:3.12-slim

# Définir le dossier de travail
WORKDIR /projet_ing_2025

# Copier les fichiers du projet dans l'image Docker
COPY . /projet_ing_2025

# Installer les dépendances (feedparser et requests)
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter le script principal au démarrage du conteneur
CMD ["python", "exercice_final.py"]
