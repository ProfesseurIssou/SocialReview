from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import Union
from datetime import datetime
try:
    from Database import Database, Base_Platform, Base_Repport_Tag, Base_Repport
except ImportError:
    from .Database import Database, Base_Platform, Base_Repport_Tag, Base_Repport


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
@app.route('/account/<int:repport_account_id>') 
def account(repport_account_id: int):
    return render_template('account.html', repport_account_id=repport_account_id)
#########


# API #
@app.route('/api/search', methods=['POST'])
def search():
    """
        - POST /api/search
        - Search for repports
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



@app.route("/api/repports", methods=['GET'])
def get_repports():
    repports = db.Repport_GetAll()
    return repports
# @app.route("/api/repport", methods=['POST'])
# def post_repport():
#     """
#         - POST /api/repport
#         - Create a new repport
#         - Request Body: {
#             "account_id": int,  # Can be null
#             "platform_id": int,
#             "tag_id": int,
#             "url": str,
#             "text": str
#     """
#     repport = request.get_json()
#     account_id = repport.get("account_id")
#     platform_id = repport.get("platform_id")
#     tag_id = repport.get("tag_id")
#     url = repport.get("url")
#     text = repport.get("text")

#     # Check if account_id exists
#     is_new_account: bool = False
#     if account_id:
#         account = db.Account_GetBy_ID(account_id)
#         if not account:
#             is_new_account = True
#     else:
#         is_new_account = True

#     # Check if platform_id exists
#     platform = db.Platform_GetBy_ID(platform_id)
#     if not platform:
#         return {"error": "Platform not found"}
    
#     # Check if tag_id exists
#     tag = db.Repport_Tag_GetBy_ID(tag_id)
#     if not tag:
#         return {"error": "Tag not found"}
    
#     # Create new account if not exists


#     db.Repport_Insert(repport)
#     return repport

#######


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
