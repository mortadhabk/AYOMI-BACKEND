# CHEMIN_DU_FICHIER: /AYOMI-BACKEND/Dockerfile
# Utiliser l'image de base Python 3.9
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /code

# Copier le fichier requirements
COPY ./requirements.txt /code/requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copier le code source
COPY ./src /code/src

# Définir le répertoire de travail sur le répertoire du code source
WORKDIR /code/src

# Commande pour exécuter l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
