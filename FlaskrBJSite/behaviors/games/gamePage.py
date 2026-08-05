#This contains the logic for repeated gameplay

from flask import(
    Blueprint,flash,g,redirect,render_template,request,url_for, session
)
from werkzeug.exceptions import abort
from FlaskrBJSite.behaviors.auth import login_required
from FlaskrBJSite.Database import db
from FlaskrBJSite.behaviors.games.blackjack import BlackJack

bp = Blueprint('games',__name__)
# bj = BLACKJACK TODO make this connect to the blackjack page
balance = "Balance"
BJGame = "BJGame"
bettingAmount = "BettingAmount"
gameNumber = "GameNumber"
def setupGameSession():
    session[balance] = 100
    session[BJGame] = 123
    session[bettingAmount] = 0
    session[gameNumber] = 0

@bp.route('/betting',methods=('GET','POST'))
@login_required
def betting():
    setupGameSession()
    if request.method == 'POST':
        print('1')
        betAmount = int(request.form['betting'])
        error = None
        print('2')
        if betAmount > int(session[balance]):
            print('3')
            error = "Not enough for bet"
        if betAmount == 0:
            print('4')
            error = "Must bet at least 1"
        if error is not None:
            print('5')
            flash(error)
        else:
            print('6')
            session[bettingAmount] = betAmount
            # session[BJGame] = BlackJack().createDictonarySave()
            print('7')
            print(dict(session))
            return redirect(url_for('games.playing'))
    return render_template('games/betting.html')

@bp.route('/playing',methods=('GET','POST'))
@login_required
def playing():#TODO: refactor to better use the tools provided
    print('8')
    if request.method == 'POST':
        if request.form['playerChoice'] == "Hit":
            session[BJGame].hit()
            if session[BJGame].gameStillPlaying():
                return redirect(url_for('games.playing.html'))
            else:
                endOfHandHandler()
        elif request.form['playerChoice'] == "Stay":
            session[BJGame].stand()
            endOfHandHandler()
    return render_template('games/playing.html')  # ''',cards = session[BJGame].getCards()'''

def endOfHandHandler():
    if session[BJGame].didPlayerWin():
        session[balance] += session[bettingAmount]
    else:
        session[balance] -= session[bettingAmount]

    session[gameNumber] += 1
    return redirect(url_for('games.results'))


@bp.route('/results',methods=('GET','POST'))
@login_required
def results():
    return render_template('games/results.html')

@bp.route("/finalScoring")
@login_required
def finalScoring():
    if request.method == 'POST':
        if request.form['playerChoice'] == "Save Score":
            db.saveScore(session['user_id'],session[balance])
            return render_template('games/finalScoring.html',scoreSaved = False)
    return render_template('games/finalScoring.html',scoreSaved = True)