from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import Union
from datetime import datetime
try:
    from Database import Database, Base_Platform, Base_Repport_Tag, Base_Repport, Base_Repport_Account
except ImportError:
    from .Database import Database, Base_Platform, Base_Repport_Tag, Base_Repport, Base_Repport_Account


app = Flask(__name__)

# ROUTE #
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/account/<int:account_id>')
def account(account_id: int):
    return render_template('account.html')
#########


# API #
#######


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
