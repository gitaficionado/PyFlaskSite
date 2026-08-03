#This contains the logic for repeated gameplay

from flask import(
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from werkzeug.exceptions import abort
from FlaskrBJSite.behaviors.auth import login_required
from FlaskrBJSite.Database.db import get_db
from FlaskrBJSite.behaviors.games.blackjack import BlackJack

bp = Blueprint('games',__name__)
# bj = BLACKJACK TODO make this connect to the blackjack page
@bp.route('/betting',methods=('GET','POST'))
def betting():
    if request.method == 'POST':
        betAmount = request.form['betting']

        error = None
        if betAmount > g.balance:
            error = "Not enough for bet"
        if betAmount == 0:
            error = "Must bet at least 1"
        if error is not None:
            flash(error)
        else:
            g.betAmount = betAmount
            g.BJGame = BlackJack()
            return render_template('games/playing.html',cards = g.BJGame.getCards())
    return render_template('games/betting.html')

@bp.route('/playing',methods=('GET','POST'))
def playing():
    if request.method == 'POST':
        if request.form['playerChoice'] == "Hit":
            g.BJGame.hit()
            if g.BJGame.gameStillPlaying():
                return render_template('games/playing.html', cards=g.BJGame.getCards())
            else:
                if g.BJGame.didPlayerWin():
                    g.balance += g.betAmount
                else:
                    g.balance -= g.betAmount
                if g.gameNumber < 10 and g.balance >0: #THIS IS THE NUMBER KEEPING TRACK OF HOW MANY GAMES OF BJ THEY CAN PLAY
                    g.gameNumber +=1
                    return render_template('games/betting.html')
                else:
                    return render_template('games/scoring.html')
        elif request.form['playerChoice'] == "Stay":
            g.BJGame.stand()
            if g.BJGame.didPlayerWin():
                g.balance += g.betAmount
            else:
                g.balance -= g.betAmount
            return render_template('games/betting.html')
    return render_template('games/playing.html',cards = g.BJGame.getCards())