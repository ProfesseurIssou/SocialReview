from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import Union
from datetime import datetime
try:
    from Database import Database, Base_Platform, Base_Report_Tag, Base_Report
except ImportError:
    from .Database import Database, Base_Platform, Base_Report_Tag, Base_Report


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
    results = [result for result in results if username in result["username"]]

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
    return {
        "score": 0,
        "interpretation": "No report",
        "reports": []
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
    """
    report = request.get_json()
    account_id = report.get("account_id")
    tag_id = report.get("tag_id")
    text = report.get("text")
    

    db.Report_Insert(
        account_id=account_id,
        report_date=datetime.now(),
        report_tag_id=tag_id,
        report_text=text
    )
    return report
#######


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
