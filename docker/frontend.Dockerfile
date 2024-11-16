# Étape de build
FROM node:18-alpine as build

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers package.json et package-lock.json
COPY frontend/package*.json ./

# Installation des dépendances
RUN npm install

# Copie du code source
COPY frontend/ .

# Build de l'application
RUN npm run build

# Étape de production
FROM nginx:alpine

# Copie des fichiers de build
COPY --from=build /app/build /usr/share/nginx/html

# Copie de la configuration nginx (si nécessaire)
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Exposition du port
EXPOSE 80

# Démarrage de nginx
CMD ["nginx", "-g", "daemon off;"]
