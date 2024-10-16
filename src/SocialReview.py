from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np
from typing import Union
from datetime import datetime, date, timedelta
try:
    from Database import Database, Base_Platform, Base_Report_Tag, Base_Report
except ImportError:
    from .Database import Database, Base_Platform, Base_Report_Tag, Base_Report
import re
import emoji

app = Flask(__name__)
db = Database()


def MOCK_SEARCH():
    """
        - Mock recherches twitter, facebook, instagram, discord
    """
    return [
        {"id": "526433", "platform": "twitter", "username": "vidou", "url": "https://twitter.com/vidou"},
        {"id": "66465", "platform": "facebook", "username": "vidou", "url": "https://facebook.com/vidou"},
        {"id": "#7755", "platform": "instagram", "username": "vidou", "url": "https://instagram.com/vidou"},
        {"id": "854654354", "platform": "twitter", "username": "mahat", "url": "https://twitter.com/mahat"},
        {"id": "23213", "platform": "facebook", "username": "mahat", "url": "https://facebook.com/mahat"},
        {"id": "531323522", "platform": "twitter", "username": "professeurissou", "url": "https://twitter.com/professeurissou"},
    ]




def sanitize_text(text: str) -> str:
    """
    Cette fonction prend un texte en entrée et remplace certaines parties par des # :
    - Émojis
    - Adresse email
    - Numéro de téléphone
    - Lien externe
    - Nom ou prénom
    - Ascii art (en se basant sur des caractères souvent utilisés)
    """

    # Remplacer les émojis
    def replace_emoji(text: str) -> str:
        return ''.join('#' if emoji.is_emoji(char) else char for char in text)

    # Remplacer les emails
    def replace_email(text: str) -> str:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_regex, '#', text)

    # Remplacer les numéros de téléphone
    def replace_phone(text: str) -> str:
        phone_regex = r'(\+?\d{1,2}[-.\s]?)?(\(?\d{1,4}\)?[-.\s]?)?(\d{1,4}[-.\s]?){2,3}\d{1,4}'
        return re.sub(phone_regex, '#', text)

    # Remplacer les liens externes
    def replace_url(text: str) -> str:
        url_regex = r'(https?://[^\s]+)'
        return re.sub(url_regex, '#', text)

    # Remplacer les noms ou prénoms (en supposant des noms et prénoms communs français)
    def replace_names(text: str) -> str:
        names = ['Jean', 'Marie', 'Pierre', 'Paul', 'Sophie', 'Lucas', 'Emma', 'Chloé']  # Vous pouvez enrichir cette liste
        for name in names:
            text = re.sub(r'\b' + name + r'\b', '#', text, flags=re.IGNORECASE)
        return text

    # Chaînage des remplacements
    text = replace_emoji(text)
    text = replace_email(text)
    text = replace_phone(text)
    text = replace_url(text)
    text = replace_names(text)

    return text




# ROUTE #
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/account/<int:report_account_id>') 
def account(report_account_id: int):
    return render_template('account.html', report_account_id=report_account_id)
#########


# API #
@app.route('/api/search', methods=['POST'])
def search():
    """
        - POST /api/search
        - Search for reports
        - Request Body: {
            "username": str
        }
        - Response: [
            {
                "id": str,
                "platform": str,
                "username": str,
                "url": str
            }
        ]
    """
    data = request.get_json()
    username = data.get("username")
    if username == "":
        return []
    
    results = MOCK_SEARCH()
    # filter results by username
    results = [result for result in results if username.lower() in result["username"].lower()]

    return results

@app.route('/api/score/<int:report_account_id>', methods=['GET'])
def score(report_account_id: int):
    """
        - GET /api/score/<int:report_account_id>
        - Get the score of an account
        - Response: {
            "score": int,
            "interpretation": str,
            "reports": [
                {
                    "id": int,
                    "tag": str,
                    "text": str,
                    "date": str
                },
                ... 
            ]
        }
    """

    def Algorithme(date_list: list[datetime.date]) -> float:
        """
            - Algorithme de calcul de score
            - Paramètres: liste de dates [date1, date2, ...]
            - Retourne: score float
        """
        if date_list == []:
            return 0
        # Création d'un dictionnaire de dates et de leur fréquence
        date_count: dict[datetime.date, int] = {}
        for date in date_list:
            if date in date_count:
                date_count[date] += 1
            else:
                date_count[date] = 1

        # Tri du dictionnaire par date
        date_count = dict(sorted(date_count.items(), key=lambda item: item[0]))

        # Récupération de la première et dernière date
        first_date = list(date_count.keys())[0]
        last_date = datetime.now().date()

        # Création d'une liste de dates entre la première et la dernière date au format YYYY-MM-DD
        date_range = [first_date + timedelta(days=x) for x in range((last_date - first_date).days + 1)]

        # Création d'une liste de fréquences de dates
        date_freq = [date_count.get(date, 0) for date in date_range]

        # Création de la courbe de diminution (10/(x+1))
        j = len(date_freq)
        decrease_curve = [0.5/(i+0.1) for i in range(j)]

        # Calcul du score (somme du jour * valeur courbe de diminution du jour)
        date_freq = list(reversed(date_freq))
        score = np.sum(np.array(date_freq) * np.array(decrease_curve))
        return score
    
    reports = db.Report_GetBy_AccountID(report_account_id)

    date_list = [report.report_date for report in reports]
    score = Algorithme(date_list)
    

    # Palié pour l'interpretation
    """
        "Aucun rapport" = 0
        "Suspect" = 0>score>5
        "Troublefête" = 5>score>10
        "Problèmatique" = 10>score>15
    """
    if score == 0:
        interpretation = "Aucun rapport"
    elif score > 0 and score < 5:
        interpretation = "Suspect"
    elif score >= 5 and score < 10:
        interpretation = "Troublefête"
    elif score >= 10 and score < 15:
        interpretation = "Problèmatique"
    else:
        interpretation = "Dangereux"

    return {
        "score": score,
        "interpretation": interpretation,
        "reports": reports
    }









@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    platforms = db.Platform_GetAll()
    return platforms

@app.route("/api/accounts", methods=['GET'])
def get_accounts():
    accounts = db.Account_GetAll()
    return accounts
@app.route("/api/account/create", methods=['POST'])
def post_account():
    """
        - POST /api/account/create
        - Create a new account
        - Request Body: {
            "account_id": int,
            "platform_id": int,
            "url": str
        }
    """
    account = request.get_json()
    account_id = account.get("account_id")
    platform_id = account.get("platform_id")
    url = account.get("url")

    # Check if platform_id exists
    platform = db.Platform_GetBy_ID(platform_id)
    if not platform:
        return {"error": "Platform not found"}
    
    # Check if user_id exists
    db.Account_Insert(platform_id=platform_id, account_id=account_id, account_url=url)
    return True

@app.route("/api/tags", methods=['GET'])
def get_tags():
    tags = db.ReportTag_GetAll()
    return tags


@app.route("/api/reports", methods=['GET'])
def get_reports():
    reports = db.Report_GetAll()
    for report in reports:
        report.report_date = report.report_date.strftime("%Y-%m-%d")
    return reports


@app.route("/api/report", methods=['POST'])
def post_report():
    """
        - POST /api/report
        - Create a new report
        - Request Body: {
            "account_id": int,
            "tag_id": int,
            "text": str
        }
    """
    report = request.get_json()
    account_id = report.get("account_id")
    tag_id = report.get("tag_id")
    text = report.get("text")



    

    db.Report_Insert(
        account_id=account_id,
        report_date=datetime.now(),
        report_tag_id=tag_id,
        report_text=sanitize_text(text)
    )
    return report
#######

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
