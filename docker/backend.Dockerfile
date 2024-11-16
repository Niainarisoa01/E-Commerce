# Image de base Python
FROM python:3.11-slim

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Désactiver la mise en buffer de stdout/stderr
ENV PYTHONUNBUFFERED 1

# Copie des fichiers requirements
COPY backend/requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source (en excluant __pycache__)
COPY backend/ .
RUN find . -type d -name __pycache__ -exec rm -r {} +

# Exposition du port
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
