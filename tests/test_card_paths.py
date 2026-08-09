import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FlaskrBJSite.behaviors.games.gamePage import cardTranslating


def test_card_paths_match_existing_files():
    paths = cardTranslating([['Spades', 'A'], ['Hearts', '10']], True)

    assert paths[0] == 'images/cards/card_back.png'
    assert paths[1] == 'images/cards/hearts_10.png'

    for path in paths:
        full_path = os.path.join('FlaskrBJSite', 'static', path.replace('images/', ''))
        assert os.path.exists(full_path), path
