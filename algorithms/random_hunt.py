
###### Base Algorithm: Random

class Player:
    def __init__(self):
        """
        The Reputation Hunter

        The chance of hunting is entirely based off of the opponent's reputation.
        Hunt all first round.
        """

        self.random = __import__("random")

    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):
        hunt_decisions = list()
        for x in player_reputations:
            test = self.random.random()
            if test < .5:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        pass # do nothing

    def round_end(self, award, m, number_hunters):
        pass # do nothing