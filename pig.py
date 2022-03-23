import random
import argparse

random.seed(0)


# if dice lands on one
class ExceptionforOne(Exception):
    pass


# dice class
class Die:
    """Class for the die"""

    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        """Returns value of rolled dice or exception"""
        self.value = random.randint(1, 6)
        if self.value == 1:
            raise ExceptionforOne

        return self.value

    def __str__(self):
        return "Rolled " + str(self.value) + "."


class Box:
    """Holds the box value"""

    def __init__(self):
        self.value = 0

    def setToZero(self):
        self.value = 0

    def addValue(self, value_of_dice):
        self.value += value_of_dice


class Player(object):
    """Base class for different player types."""

    def __init__(self, name=None):
        self.name = name
        self.score = 0

    def add_score(self, player_score):
        """Adds score to total score."""

        self.score += player_score

    def __str__(self):
        """Returns player name and current score."""

        return str(self.name) + ": " + str(self.score)


class PigGame(Player):
    def __init__(self, name):
        super(PigGame, self).__init__(name)

    def keep_rolling(self, box):
        """Roll or hold"""

        human_decision = self.choices("  r - Roll again, h - Hold? ")
        if human_decision == "r":
            return True
        else:
            return False

    def choices(self, prompt='Please enter a Choice: '):
        """Takes input from user"""

        while True:

            choice = (input(prompt))
            if (choice != "r" and choice != "h"):
                print("Enter a valid choice")
            else:
                break
        return choice


class Play:
    def __init__(self, players):
        """Starts the game by asking names of players"""

        self.players = []

        for i in range(players):
            player_name = input('Player {}, enter your name: '.format(i + 1))
            self.players.append(PigGame(player_name))

        self.no_of_players = len(self.players)

        self.die = Die()
        self.box = Box()

    def firstPlayer(self):
        """Player to begin"""
        self.current_player = 0 % self.no_of_players

    def nextPlayer(self):
        """The next player"""
        self.current_player = (self.current_player + 1) % self.no_of_players

    def previousPlayer(self):
        """The previous player"""
        self.current_player = (self.current_player - 1) % self.no_of_players

    def get_all_scores(self):
        """Returns a join all players scores."""

        return ', '.join(str(player) for player in self.players)

    def startGame(self):
        """Plays an entire game."""

        self.firstPlayer()

        while all(player.score < 100 for player in self.players):
            print('\n Current score > {}'.format(self.get_all_scores()))
            self.box.setToZero()

            input("-------{} Press Enter to Start------  ".format(self.players[self.current_player].name))
            while self.keep_rolling():
                pass

            self.players[self.current_player].add_score(self.box.value)
            self.nextPlayer()

        self.previousPlayer()
        print(' {} hs won the game. Hurraay!! '.format(self.players[self.current_player].name).center(70, '*'))

    def keep_rolling(self):
        """ Check to see if the game is ready to start. If the dice rolls a one, reset the box to zero"""
        try:
            value_of_dice = self.die.roll()
            self.box.addValue(value_of_dice)
            print('Last roll: {}, New Turn Total: {}'.format(value_of_dice, self.box.value))

            # do you want to keep rolling?
            return self.players[self.current_player].keep_rolling(self.box)

        except ExceptionforOne:
            print('Oops, Rolled a one. Changing Player')
            self.box.setToZero()
            return False


def main():
    # Initialize parser
    commandParser = argparse.ArgumentParser(description="Send a ­­url parameter to the script")

    commandParser.add_argument("--numPlayers", type=str, help="Number of players")

    args = commandParser.parse_args()
    if not args.numPlayers:  # If the parameter isn't passed, the number of players will be 2
        no_of_players = 2
    else:
        no_of_players = int(args.numPlayers)

    startGame = Play(no_of_players)

    startGame.startGame()


if __name__ == '__main__':
    main()