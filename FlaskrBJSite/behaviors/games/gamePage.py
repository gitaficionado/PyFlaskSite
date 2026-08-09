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
    print(game.getPlayerCards())
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
    return render_template('games/playing.html',playerCards = cardTranslating(game.getPlayerCards()), dealerCards = cardTranslating(game.getDealerCards(),True))  # ''',cards = session[BJGame].getCards()'''

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
    game = BlackJack(session[BJGame])
    return render_template('games/results.html',playerCards = cardTranslating(game.getPlayerCards()), dealerCards = cardTranslating(game.getDealerCards()))

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

suitTranslator = {
    "Spades": "spades",
    "Hearts":"hearts",
    "Diamonds":"diamonds",
    "Clubs":"clubs"
}
rantTranslator = {
    "1":"1",
    "2":"2",
    "3":"3",
    "4":"4",
    "5":"5",
    "6":"6",
    "7":"7",
    "8":"8",
    "9":"9",
    "10":"10",
    "J":"jack",
    "Q":"queen",
    "K":"king",
    "A":"ace"
}
def cardTranslating(cardList,hideFirst = False):
    cardPreamble = "images/cards/"

    returnList = []
    for card in cardList:
        returnList.append(cardPreamble+suitTranslator[card[0]]+"_"+rantTranslator[card[1]]+".png")

    if hideFirst:
        returnList[0] = cardPreamble+"card_back.png"

    return returnList
