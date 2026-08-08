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
    session[BJGame] = {}
    session[bettingAmount] = 0
    session[gameNumber] = 0

@bp.route('/betting',methods=('GET','POST'))
@login_required
def betting():
    # setupGameSession()
    if request.method == 'POST':
        betAmount = int(request.form['betting'])
        error = None
        if betAmount > int(session[balance]):
            error = "Not enough for bet"
        if betAmount == 0:
            error = "Must bet at least 1"
        if error is not None:
            flash(error)
        else:
            session[bettingAmount] = betAmount
            session[BJGame] = BlackJack().createDictonarySave()
            return redirect(url_for('games.playing'))
    return render_template('games/betting.html')




@bp.route('/playing',methods=('GET','POST'))
@login_required
def playing():#TODO: refactor to better use the tools provided
    game = BlackJack(session[BJGame])
    if request.method == 'POST':
        if request.form['playerChoice'] == "Hit":
            game.hit()
            if game.gameStillPlaying():
                session[BJGame] = game.createDictonarySave()
                return redirect(url_for('games.playing'))
            else:
                return endOfHandHandler(game)
        elif request.form['playerChoice'] == "Stay":
            game.stand()
            return endOfHandHandler(game)
    return render_template('games/playing.html',cards = cardTranslating(None))  # ''',cards = session[BJGame].getCards()'''

def endOfHandHandler(bjGame):
    if bjGame.didPlayerWin():
        session[balance] += session[bettingAmount]
    elif not bjGame.isGameTie():
        session[balance] -= session[bettingAmount]

    session[gameNumber] += 1
    session[BJGame] = bjGame.createDictonarySave()
    return redirect(url_for('games.results'))


@bp.route('/results',methods=('GET','POST'))
@login_required
def results():
    return render_template('games/results.html', cards = cardTranslating(None))

@bp.route("/finalScoring" ,methods=('GET','POST'))
@login_required
def finalScoring():
    if request.method == 'POST':
        db.saveScore(session['user_id'],session[balance])
        if request.form['playerChoice'] == "New Game":
            setupGameSession()
            return redirect(url_for('games.betting'))
        else:
            return redirect(url_for('welcome'))
    return render_template('games/finalScoring.html',scoreSaved = True)


def cardTranslating(cardList):
    cardPreamble = "images/cards/"
    return [cardPreamble+"card_back.png",cardPreamble+"card_back.png"]
