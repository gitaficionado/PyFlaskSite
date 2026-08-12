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
wins = "wins"
losses = "losses"
ties = "ties"
def setupGameSession():
    session[balance] = 100
    session[BJGame] = {}
    session[bettingAmount] = 0
    session[gameNumber] = 0
    session[wins] = 0
    session[losses] = 0
    session[ties] = 0

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
        session[wins]+=1
    elif not bjGame.isGameTie():
        session[balance] -= session[bettingAmount]
        session[losses]+=1
    else:
        session[ties]+=1
    session[gameNumber] += 1
    session[BJGame] = bjGame.createDictonarySave()
    return redirect(url_for('games.results'))


@bp.route('/results',methods=('GET','POST'))
@login_required
def results():
    game = BlackJack(session[BJGame])
    resultMessage = ""
    if game.didPlayerWin():
        resultMessage = "You win the hand"
    elif not game.isGameTie():
        resultMessage = "Tie"
    else:
        resultMessage = "You Lost the hand"

    return render_template('games/results.html',playerCards = cardTranslating(game.getPlayerCards()), dealerCards = cardTranslating(game.getDealerCards()), didPlayerWin = resultMessage)

@bp.route("/finalScoring" ,methods=('GET','POST'))
@login_required
def finalScoring():
    if request.method == 'POST':
        db.saveScore(session['user_id'],session[balance],session[wins],session[losses],session[ties])
        if request.form['playerChoice'] == "Deal me in!":
            setupGameSession()
            return redirect(url_for('games.betting'))
        elif request.form['playerChoice'] == "See Leaderboard":
            return redirect((url_for('leaderboard.leaderboard')))
        else:
            return redirect(url_for('welcome'))
    return render_template('games/finalScoring.html',scoreSaved = True)

suitTranslator = {
    "Spades": "spades",
    "Hearts":"hearts",
    "Diamonds":"diamonds",
    "Clubs":"clubs",
    "spades": "spades",
    "hearts": "hearts",
    "diamonds": "diamonds",
    "clubs": "clubs"
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
    "A":"ace",
    "j":"jack",
    "q":"queen",
    "k":"king",
    "a":"ace"
}

def cardTranslating(cardList, hideFirst=False):
    cardPreamble = "images/cards/"
    returnList = []

    for card in cardList or []:
        suit = card[0] if len(card) > 0 else ''
        rank = card[1] if len(card) > 1 else ''

        suitKey = suitTranslator.get(suit, suit.lower() if isinstance(suit, str) else '')
        rankKey = rantTranslator.get(rank, rank.lower() if isinstance(rank, str) else '')

        if suitKey and rankKey:
            returnList.append(f"{cardPreamble}{suitKey}_{rankKey}.png")
        else:
            returnList.append(f"{cardPreamble}card_back.png")

    if hideFirst and returnList:
        returnList[0] = cardPreamble + "card_back.png"

    return returnList
