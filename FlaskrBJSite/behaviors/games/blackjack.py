#this contains the logic for 1 game of blackjack
import random

#key, value dict for face value of card
values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11,
}


class Card:
    def __init__(self, suit='', rank=''):
        self.suit = suit
        self.rank = rank

    def getSuit(self):
        return self.suit

    def setSuit(self, suit):
        self.suit = suit

    def getRank(self):
        return self.rank

    def setRank(self, rank):
        self.rank = rank

    # Lookup the value of a card before adjusting for the ace in a specific hand
    def getCardValue(self):
        return values[self.rank]

    def __str__(self):
        return f'({self.suit}, {self.rank})'

    # Returns the Card as a list
    def toList(self):
        return [self.suit, self.rank]

    # Creates and returns a Card with the data from the passed in list
    def fromList(self, cardList):
        self.suit = cardList[0]
        self.rank = cardList[1]
        return self


class Deck:
#list of cards, shuffled
    suits = ("Spades", "Clubs", "Hearts", "Diamonds")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

    '''
        If no list is given, build a full 52 card deck and shuffle it.
        If a list is given (from a saved game), rebuild exactly those cards
        in exactly that order, without shuffling.
    '''
    def __init__(self, savedCards=None):
        self.cards = []
        if savedCards is None:
            for suit in Deck.suits:
                for rank in Deck.ranks:
                    self.cards.append(Card(suit, rank))
            self.shuffle()
        else:
            for cardList in savedCards:
                card = Card().fromList(cardList)
                self.cards.append(card)

    def getCards(self):
        return self.cards

    def setCards(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    # Deal one card out of the deck
    def drawCard(self):
        return self.cards.pop()

    # Returns the Deck as a list of Card lists
    def toList(self):
        result = []
        for card in self.cards:
            result.append(card.toList())
        return result

class Hand:
    '''
        If no list is given, start an empty hand.
        If a list is given (from a saved game), re-add each card so that
        value and aces are recomputed automatically.
    '''
    def __init__(self, savedCards=None):
        self.cards = []
        self.value = 0
        self.aces = 0
        if savedCards is not None:
            self.fromList(savedCards)

    def getCards(self):
        return self.cards

    def setCards(self, cards):
        self.cards = cards

    def getValue(self):
        #reworking this to only return the value and not re-calculate every single time
        # self.value = 0
        # for c in self.cards:
        #     self.value += c.getCardValue()
        #     print("current Value" + str(self.value)+" card value"+str(c.getCardValue()))
        # self.adjust_for_ace()
        # print(self.value)
        return self.value

    def getAces(self):
        return self.aces

    def addCard(self, card):
        self.cards.append(card)
        print("Old value is: "+str(self.value))
        # recompute value of the hand after adding the card by calling getValue() before adjusting for ace
        self.value += card.getCardValue()
        if card.getRank() == "A":
            self.aces += 1

        #do ace handling here
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
        print("Added card:"+card.getRank()+" New value is: "+str(self.value))

    def adjust_for_ace(self):
        for i in range(self.aces):
            while self.value > 21 and self.aces:
                self.value -= 10

    # Returns the Hand as a list of [suit, rank] card lists
    def toList(self):
        result = []
        for card in self.cards:
            result.append(card.toList())
        return result

    # Uses the passed in list of card lists parameter,
    # one [suit, rank] list per card, to initialize the hand
    def fromList(self, cards):
        for cardList in cards:
            card = Card().fromList(cardList)
            self.addCard(card)


class Player:
    def __init__(self, playerID='', savedCards=None):
        self.ID = playerID
        self.hand = Hand(savedCards)

    def getID(self):
        return self.ID

    def setID(self, playerID):
        self.ID = playerID

    # Return the hand currently held by the player as a list of Cards
    def getHand(self):
        return self.hand.getCards()

    def setHand(self, hand_cards):
        self.hand.setCards(hand_cards)

    # Return the value of the hand currently held by the player
    def getValue(self):
        # print("Player get value call")
        return self.hand.getValue()

    # Adds the card passed in to the player's hand
    # without drawing from the deck (e.g. when loading a game)
    def addCard(self, card):
        self.hand.addCard(card)

    def hit(self, deck):
        self.addCard(deck.drawCard())

    # Returns the player data as a list
    def toDictionary(self):
        return { 'playerID': self.ID, 'hand': self.hand.toList() }


class Dealer(Player):

    def play_turn(self, deck):
        # print("dealer get value call")
        while self.getValue() < 17:
            self.hit(deck)

#a single game (hand) of Blackjack, playable through the Flask routes
class BlackJack:

    resultOptions = ('Player wins', 'Player busts',
                     'Dealer wins', 'Dealer busts', 'Push', '')

    '''
        If no dictonary is given, create a new fresh game from the start
        If a dictonary is given, uses the dictonary to set all the game values
    '''
    def __init__(self, dictionaryLoadIn=None):
        if dictionaryLoadIn is not None:
            #load an existing game back using the passed in dictionary parameter
            self.fromDictionary(dictionaryLoadIn)
        else:
            #fresh game: new shuffled deck, player and dealer, initial deal of two cards each
            self.deck = Deck()
            self.player = Player('Player')
            self.dealer = Dealer('Dealer')
            self.gameFinished = False
            self.result = ''
            self.deal()

    # Initialize game from passed in dictionary
    def fromDictionary(self, dictionaryLoadIn):
            self.setDeck(Deck(dictionaryLoadIn['deck']))
            self.setPlayer(Player(dictionaryLoadIn['player']['playerID'], dictionaryLoadIn['player']['hand']))
            self.setDealer(Dealer(dictionaryLoadIn['dealer']['playerID'], dictionaryLoadIn['dealer']['hand']))
            self.setGameFinished(dictionaryLoadIn['gameFinished'])
            self.setResult(dictionaryLoadIn['result'])

    # Return the game data to caller as a dictionary
    def toDictionary(self):
        return {'deck': self.deck.toList(),
                'player': self.player.toDictionary(),
                'dealer': self.dealer.toDictionary(),
                'gameFinished': self.gameFinished,
                'result': self.result}

    '''
        Creates and returns a dictonary saving off all of the game veriables in
        a way such that the blackJack object can remain in the same state as
        when the dictornay is created
    '''
    def createDictonarySave(self):
        return self.toDictionary()

    #----------------- getters and setters -----------------

    def getDeck(self):
        return self.deck

    def setDeck(self, deck):
        self.deck = deck

    def getPlayer(self):
        return self.player

    def setPlayer(self, player):
        self.player = player

    def getDealer(self):
        return self.dealer

    def setDealer(self, dealer):
        self.dealer = dealer

    def getResult(self):
        return self.result

    def setResult(self, resultoption):
        if resultoption in BlackJack.resultOptions:
            self.result = resultoption
        return self.result

    def getGameFinished(self):
        return self.gameFinished

    def setGameFinished(self, finished):
        self.gameFinished = finished

    '''
    Get the cards in the player's hand as a list of card [suit, rank] lists
    '''
    def getPlayerCards(self):
        result = []
        for c in self.player.getHand():
            result.append(c.toList())
        return result

    '''
    Get the cards in the dealer's hand as a list of card [suit, rank] lists
    '''
    def getDealerCards(self):
        result = []
        for c in self.dealer.getHand():
            result.append(c.toList())
        return result

    #----------------- game play -----------------

    def deal(self):
#initial deal of two cards each
        for i in range(2):
            self.player.addCard(self.deck.drawCard())
            self.dealer.addCard(self.deck.drawCard())

    '''
        The "Hit" game action, with the assumption that it is legal at the time
    '''
    def hit(self):
        self.player.hit(self.deck)
        # print("Player get value call in HIT")
        if self.player.getValue() > 21:
            self.result = 'Player busts'
            self.gameFinished = True

    '''
        The "Stand" game action, with the assumption that it is legal at the time
    '''
    def stand(self):
#to play the dealer turn and decide the result
        self.dealer.play_turn(self.deck)
        # print("Dealer get value call in Stand")
        dealerValue =  self.dealer.getValue()
        # print("Player get value call in Stand")
        playerValue = self.player.getValue()
        if dealerValue > 21:
            self.result = 'Dealer busts'
        elif dealerValue>playerValue:
            self.result = 'Dealer wins'
        elif dealerValue < playerValue:
            self.result = 'Player wins'
        else:
            self.result = 'Push'
        self.gameFinished = True

    '''
        returns True if the player has won the hand
        Returns False otherwide (Tie or Lose)
    '''
    def didPlayerWin(self):
        return self.result in ('Player wins', 'Dealer busts')

    '''
        Returns True if the player tied
        Return Flase otherwise (Win or Lose)
    '''
    def isGameTie(self):
        return self.result == 'Push'

    '''
        Returns True if the hand is still playing, as in the player still has the ability to hit/stand
        Returns False if the hand is over and a winner has been decided
    '''
    def gameStillPlaying(self):
        return not self.gameFinished