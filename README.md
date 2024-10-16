# SocialReview API

SocialReview est une application Flask qui permet de gérer des plateformes, des comptes, et des rapports. Ce projet offre plusieurs endpoints d'API pour interagir avec ces données.

## Prérequis

- Docker
- Python 3.x (facultatif pour exécuter en local sans Docker)
- Flask
- SQLite

## Installation

1. Clonez ce dépôt.

```bash
git clone https://github.com/votre-compte/socialreview.git
cd socialreview
```

2. Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

3. Exécutez l'application :

```bash
python SocialReview.py
```

L'application sera disponible à l'adresse suivante : `http://127.0.0.1:5001`

## Utilisation avec Docker

### 1. Construction et exécution avec Docker

Vous pouvez également exécuter cette application en utilisant Docker et Docker Compose.

1. Assurez-vous d'avoir Docker installé sur votre machine.
2. Cloner le dépôt :

```bash
git clone https://github.com/votre-compte/socialreview.git
cd socialreview
```

3. Construire l'image Docker et lancer le conteneur :

```bash
docker-compose up --build
```

Cela va automatiquement :
- Construire l'image Docker à partir du fichier `Dockerfile`.
- Exécuter l'application dans un conteneur.

L'application sera disponible à `http://localhost:5001`.

## Déploiement automatique avec GitHub Actions

### 1. Configuration de GitHub Actions pour déploiement

Le projet contient un fichier `docker-publish.yml` dans le répertoire `.github/workflows/`, qui est configuré pour effectuer un build et un push de l'image Docker sur DockerHub à chaque mise à jour du dépôt.

#### Étapes pour configurer le déploiement :

1. **Créer un compte DockerHub** (si vous n'en avez pas déjà un).
2. **Ajouter vos secrets GitHub** :
   - Allez dans votre dépôt GitHub, puis dans `Settings > Secrets and variables > Actions`.
   - Ajoutez deux secrets : 
     - `DOCKER_USERNAME`: Votre nom d'utilisateur DockerHub.
     - `DOCKER_PASSWORD`: Votre mot de passe DockerHub.
3. **Pousser une modification** dans la branche `main` ou déclencher manuellement une action depuis l'onglet `Actions` de GitHub.

### 2. GitHub Actions

Le fichier `docker-publish.yml` va :
- Construire l'image Docker à partir du fichier `Dockerfile`.
- Pousser l'image sur DockerHub à chaque commit ou déclenchement manuel.

```yaml
name: Publish Docker image

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Log in to DockerHub
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build Docker image
        run: docker build . -t your-dockerhub-username/socialreview

      - name: Push Docker image to DockerHub
        run: docker push your-dockerhub-username/socialreview
```


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



# Algorithme de Calcul du Score de réputation

L'objectif de cet algorithme est de calculer un **score de réputation** basé sur une liste de dates, où chaque date représente un signalement d'incident. Le score est calculé en tenant compte de la fréquence des signalements et de l'ancienneté des incidents, avec un poids décroissant attribué aux signalements plus anciens.

## Description de l'Algorithme

L'algorithme prend en entrée une liste de dates (`date_list`) et retourne un score qui reflète la gravité du profil basé sur ces signalements.

<!-- image -->
![Algorithme de Calcul du Score de Réputation](img/formule_math.png)

### Exemple de Calcul

Si l'on a la liste de dates suivante : 
```python
[2024-01-01, 2024-01-02, 2024-01-02, 2024-05-01]
```

L'algorithme :
1. Crée une plage de dates entre le 2024-01-01 et la date actuelle.
2. Compte la fréquence des signalements par jour.
3. Applique la courbe de pondération décroissante aux jours, en donnant plus de poids aux signalements récents.
4. Calcule la somme pondérée pour obtenir le score final.

### Conclusion

Cet algorithme permet de calculer un score de répuration en tenant compte à la fois de la **fréquence des signalements** et de leur **ancienneté**, en accordant plus de poids aux signalements récents. Ce score peut être utilisé pour déterminer la gravité potentielle d'un profil ou d'une situation.