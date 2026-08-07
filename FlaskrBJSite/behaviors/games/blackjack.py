#this contains the logic for 1 game of blackjack
#need to decide how to tell if the player won
class BlackJack:

    #creats and shuffles up a new game of blackjack
    #should deal out the inital cards
    #this will need to be able to load itself up from a dictonary that it created so that it can be saved

    '''
        If no dictonary is given, create a new fresh game from the start
        If a dictonary is given, uses the dictonary to set all the game values
    '''
    def __init__(self, dictonaryLoadIn={}):
        pass

    '''
    Get the cards in the players and return them as a list
    '''
    def getCards(self):
        pass
    '''
    Get the cards in the dealers and return them as a list
    '''
    def getDealerCards(self):
        pass
    '''
    The player will do a "HIT" option, with the assumption that it is legal at the time
    No return needed
    '''
    def hit(self):
        pass
    '''
        The player will do a "Stand"/"Stay" option, with the assumption that it is legal at the time
        No return needed
    '''
    def stand(self):
        pass
    '''
        returns True if the player has won the hand
        Returns False otherwide (Tie or Lose)
    '''
    def didPlayerWin(self):
        pass
    '''
        Returns True if the player tied
        Return Flase otherwise (Tie or Lose)
    '''
    def isGameTie(self):
        pass
    '''
        Returns True if the hand is still playing, as in the player still has the ability to hit/stand
        Returns False if the hand is over and a winner has been decided
    '''
    def gameStillPlaying(self):
        pass

    '''
        Creates and returns a dictonary saving off all of the game veriables in 
        a way such that the blackJack object can be remain in the same state as 
        when the dictornay is created
    '''
    def createDictonarySave(self):
        pass


