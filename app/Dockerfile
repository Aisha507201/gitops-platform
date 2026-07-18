FROM python:3.12-alpine

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code de l'application
COPY . .

EXPOSE 5000

# Commande de démarrage avec gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]