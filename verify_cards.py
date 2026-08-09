import os
import sys
sys.path.insert(0, os.getcwd())
from FlaskrBJSite.behaviors.games.gamePage import cardTranslating

print(cardTranslating([['Spades','A'], ['Hearts','10']], True))
print(os.path.exists(os.path.join('FlaskrBJSite','static','images','cards','hearts_10.png')))
