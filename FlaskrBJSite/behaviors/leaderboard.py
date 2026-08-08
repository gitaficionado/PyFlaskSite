import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from FlaskrBJSite.behaviors.games.gamePage import setupGameSession
from ..Database import db

bp = Blueprint('leaderboard', __name__, url_prefix='/lb')

@bp.route("/leaderboard")
def leaderboard():
    return render_template('leaderboard/leaderboard.html', board = db.getLeaderBoard(10))