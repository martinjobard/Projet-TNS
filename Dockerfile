# 1. On part d'une image Python légère officielle (version 3.12 comme ton venv)
FROM python:3.12-slim

# 2. On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. On copie le fichier requirements.txt D'ABORD (pour optimiser le cache Docker)
COPY requirements.txt .

# 4. On installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout le reste de ton code dans le conteneur
COPY . .

# 6. On expose le port 5000 (le port standard de Flask)
EXPOSE 5000

# 7. La commande pour lancer l'application
# --host=0.0.0.0 est OBLIGATOIRE pour que le site soit accessible depuis l'extérieur du conteneur
CMD ["flask", "run", "--host=0.0.0.0"]