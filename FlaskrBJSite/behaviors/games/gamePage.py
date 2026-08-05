#This contains the logic for repeated gameplay

from flask import(
    Blueprint,flash,g,redirect,render_template,request,url_for, session
)
from werkzeug.exceptions import abort
from FlaskrBJSite.behaviors.auth import login_required
from FlaskrBJSite.Database.db import get_db
from FlaskrBJSite.behaviors.games.blackjack import BlackJack

bp = Blueprint('games',__name__)
# bj = BLACKJACK TODO make this connect to the blackjack page
balance = "Balance"
BJGame = "BJGame"
bettingAmount = "BettingAmount"
gameNumber = "GameNumber"
def setupGameSession():
    session[balance] = 100
    session[BJGame] = None
    session[bettingAmount] = 0
    session[gameNumber] = 0

@bp.route('/betting',methods=('GET','POST'))
def betting():
    if request.method == 'POST':
        betAmount = request.form['betting']

        error = None
        if betAmount > session[balance]:
            error = "Not enough for bet"
        if betAmount == 0:
            error = "Must bet at least 1"
        if error is not None:
            flash(error)
        else:
            session[betAmount] = betAmount
            session[BJGame] = BlackJack()
            return render_template('games/playing.html',cards = session[BJGame].getCards())
    return render_template('games/betting.html')

@bp.route('/playing',methods=('GET','POST'))
def playing():
    if request.method == 'POST':
        if request.form['playerChoice'] == "Hit":
            session[BJGame].hit()
            if session[BJGame].gameStillPlaying():
                return render_template('games/playing.html', cards=session[BJGame].getCards())
            else:
                endOfHandHandler()
        elif request.form['playerChoice'] == "Stay":
            session[BJGame].stand()
            endOfHandHandler()
    return render_template('games/playing.html',cards = session[BJGame].getCards())

def endOfHandHandler():
    if session[BJGame].didPlayerWin():
        session[balance] += session[bettingAmount]
    else:
        session[balance] -= session[bettingAmount]
    if session[gameNumber] < 10 and session[balance] > 0:  # THIS IS THE NUMBER KEEPING TRACK OF HOW MANY GAMES OF BJ THEY CAN PLAY
        session[gameNumber] += 1
        return render_template('games/betting.html')
    else:
        return render_template('games/scoring.html')

