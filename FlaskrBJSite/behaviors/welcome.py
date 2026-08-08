from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from FlaskrBJSite.behaviors.games.gamePage import setupGameSession

bp = Blueprint('welcome', __name__)

@bp.route("/",methods=('GET','POST'))
def welcome():
    # 'games.betting'
    print("test")
    if request.method == 'POST':
        setupGameSession()
        return redirect(url_for('games.betting'))
    return render_template('welcome.html')
