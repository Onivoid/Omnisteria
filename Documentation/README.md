# Techs Fatfood

## Backend

### Technologies

- **Langage :** Python
- **Framework :** FastAPI
- **ORM :** Tortoise
- **Base de données :** PostgreSQL
- **Déploiement :** Docker

## Frontend

### Technologies

- **Framework JS :** NextJS
- **Librairie JS :** React
- **Librairie de Composants :** PrimeReact
- **Librairie CSS :** Aucunes
- **Pré-processeur CSS :** SCSS
- **Déploiement :** Vercel
- **Autre Techs :**
  - [Lottie](https://lottiefiles.com/) - Animations Assets
  - [Framer Motion](https://www.framer.com/motion) - Animations Components

## Classes

- **Classe User :**
  - `id: str`, *(UUID)*
  - `name: str`,
  - `email: str`, *(Nullable si inscrit via Discord / autre Provider ?)*
  - `discord_id: int`, *(Nullable si non-lié ?)*
  - `password: str`, *(Authentification passwordless ?)*
  - `created_at: date`,