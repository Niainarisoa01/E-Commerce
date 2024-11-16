# E-commerce API & Frontend

Une application e-commerce complète avec une API FastAPI et un frontend React.

## 🚀 Technologies Utilisées

### Backend
- FastAPI (Python 3.11)
- SQLAlchemy (ORM)
- SQLite (Base de données)
- Pydantic (Validation des données)
- JWT (Authentification)

### Frontend
- React
- TypeScript
- Redux Toolkit
- React Router
- Axios
- TailwindCSS

### Infrastructure
- Docker & Docker Compose
- Nginx
- Git

## 📁 Structure du Projet

```
ecommerce-project/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints API
│   │   ├── core/         # Configuration
│   │   ├── db/           # Base de données
│   │   ├── models/       # Modèles SQLAlchemy
│   │   ├── schemas/      # Schémas Pydantic
│   │   └── services/     # Services
│   ├── tests/
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── store/
│   └── package.json
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── nginx.conf
└── docker-compose.yml
```

## 🛠 Installation

### Prérequis
- Docker et Docker Compose
- Python 3.11+
- Node.js 18+
- Git

### Configuration

1. Cloner le repository :
```bash
git clone https://github.com/Niainarisoa01/E-Commerce.git
cd ecommerce-project
```

2. Configuration du backend :
```bash
cd backend
cp .env.example .env
# Modifier les variables dans .env selon vos besoins
```

3. Configuration du frontend :
```bash
cd frontend
cp .env.example .env
```

### Démarrage

Avec Docker (recommandé) :
```bash
docker-compose up --build
```

Sans Docker :

Backend :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend :
```bash
cd frontend
npm install
npm start
```

## 📚 Documentation API

La documentation de l'API est disponible aux endpoints suivants :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## 🔑 Endpoints Principaux

### Authentication
- POST `/api/auth/register` - Inscription
- POST `/api/auth/login` - Connexion

### Produits
- GET `/api/products` - Liste des produits
- GET `/api/products/{id}` - Détails d'un produit
- POST `/api/products` - Créer un produit

### Panier
- GET `/api/cart` - Voir le panier
- POST `/api/cart/items` - Ajouter au panier
- DELETE `/api/cart/items/{id}` - Supprimer du panier

### Commandes
- GET `/api/orders` - Liste des commandes
- POST `/api/orders` - Créer une commande

## 🔒 Variables d'Environnement

### Backend (.env)
```env
# Base
API_V1_STR=/api
PROJECT_NAME="E-commerce API"

# Database
SQLITE_DATABASE_URL=sqlite:///./e_commerce.db

# Security
SECRET_KEY=votre_clé_secrète_très_longue_et_complexe_à_changer_en_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

```

## 🧪 Tests

Backend :
```bash
cd backend
pytest
```

Frontend :
```bash
cd frontend
npm test
```

## 🚀 Déploiement

1. Construire les images :
```bash
docker-compose build
```

2. Démarrer les services :
```bash
docker-compose up -d
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Votre nom (@votre-github)

## 🙏 Remerciements

- FastAPI
- React
- Et tous les contributeurs open source
