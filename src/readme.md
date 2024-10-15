# SocialReview API

SocialReview est une application Flask qui permet de gérer des plateformes, des comptes, et des rapports. Ce projet offre plusieurs endpoints d'API pour interagir avec ces données.

## Prérequis

- Python 3.x
- Flask
- SQLite

## Installation

1. Clonez ce dépôt.

2. Installez les dépendances nécessaires :

```bash
pip install Flask
```

3. Exécutez l'application :

```bash
python SocialReview.py
```

L'application sera disponible à l'adresse suivante : `http://127.0.0.1:5001`

## Endpoints

### 1. **GET `/api/platforms`**
- **Description**: Récupère toutes les plateformes.
- **Réponse**: 
    - Liste des plateformes (id, nom, base_url).

### 2. **POST `/api/search`**
- **Description**: Effectue une recherche sur un nom d'utilisateur sur différentes plateformes.
- **Corps de la requête**: 
    ```json
    {
        "username": "nom_utilisateur"
    }
    ```
- **Réponse**:
    - Liste des comptes correspondants avec les champs suivants :
        - `id`: Identifiant unique du compte.
        - `platform`: Nom de la plateforme (Twitter, Facebook, etc.).
        - `username`: Nom d'utilisateur.
        - `url`: Lien vers le profil.

### 3. **GET `/api/score/<int:report_account_id>`**
- **Description**: Récupère le score d'un compte en fonction des rapports associés.
- **Réponse**:
    ```json
    {
        "score": int,
        "interpretation": "string",
        "reports": [
            {
                "id": int,
                "tag": str,
                "text": str,
                "date": str
            }
        ]
    }
    ```

### 4. **GET `/api/accounts`**
- **Description**: Récupère tous les comptes enregistrés dans la base de données.
- **Réponse**: 
    - Liste des comptes (id, platform_id, account_id, account_url).

### 5. **POST `/api/account/create`**
- **Description**: Crée un nouveau compte.
- **Corps de la requête**:
    ```json
    {
        "account_id": "identifiant_du_compte",
        "platform_id": "identifiant_de_la_plateforme",
        "url": "url_du_compte"
    }
    ```
- **Réponse**:
    - Succès ou message d'erreur.

### 6. **GET `/api/tags`**
- **Description**: Récupère tous les tags de rapport.
- **Réponse**:
    - Liste des tags (id, tag_name).

### 7. **GET `/api/reports`**
- **Description**: Récupère tous les rapports de la base de données.
- **Réponse**:
    - Liste des rapports (id, account_id, report_date, report_tag_id, report_text).

### 8. **POST `/api/report`**
- **Description**: Crée un nouveau rapport pour un compte.
- **Corps de la requête**:
    ```json
    {
        "account_id": int,
        "tag_id": int,
        "text": str
    }
    ```
- **Réponse**:
    - Le rapport créé ou un message d'erreur.

## Routes HTML

### 9. **GET `/`**
- **Description**: Affiche la page d'accueil.

### 10. **GET `/account/<int:report_account_id>`**
- **Description**: Affiche la page de détails d'un compte.

## Structure du projet

```
.
├── SocialReview.py           # Fichier principal de l'application Flask
├── Database/                 # Gestion de la base de données
├── templates/                # Contient les templates HTML pour Flask
│   ├── index.html            # Page d'accueil
│   └── account.html          # Page de détails d'un compte
└── README.md                 # Ce fichier
```

## Exécution

```bash
python SocialReview.py
```
