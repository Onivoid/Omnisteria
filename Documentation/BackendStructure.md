```md
backend/
    .gitignore
    app/
        main.py  *# Point d'entrée de l'application FastAPI*
        api/  *# Contient les routes de l'API*
            __init__.py
            route1.py
            route2.py
            ...
        models/  *# Contient les modèles Tortoise ORM*
            __init__.py
            model1.py
            model2.py
            ...
        config/
            __init__.py
            settings.py  *# Contient les paramètres de l'application (par exemple, les paramètres de la base de données)*
    template.env
    .env
    migrations/  *# Contient les fichiers de migration de la base de données*
    tests/ *# Contient les tests de l'application*
    docker-compose.yml
    Dockerfile
    requirements.txt
    venv/
```