import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ..Database import db

bp = Blueprint('welcome', __name__)

@bp.route("/")
def welcome():
    print("test")
    return render_template('welcome.html')