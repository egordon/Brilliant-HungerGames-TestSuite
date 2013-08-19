

class Player:
    def __init__(self):
        """
        Initialize all arrays and set magic numbers.
        NOTE: All "magic" numbers were calibrated using a self-programmed testing suite.
        """

        ### MAGIC NUMBERS ###
        
        # How many rounds to track at a time 
        # (also, how many rounds to wait until we start using the correlation coefficient)
        self.history = 25

        # Used for "nice" edge detection.
        # If reputation is greater than 1-edges, we hunt
        # If reputation is less than edges, we slack
        self.edges = .1

        ### END MAGIC NUMBERS ###

        # Initialize Modules
        self.scipy = __import__("scipy.stats")
        self.random = __import__("random")

        # Initialize Self-Reputation History List
        self.repArr = [x for x in range(self.history)]
        # Initialize Utility History List
        self.utilArr = [x for x in range(self.history)]

        # Initialize Correlation Coefficient
        # (Coefficient, Significance <higher is less significant>)
        self.corrcoef = (0.0, 0.0)


    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):
        """
        Self-Reputation / Utility Correlation Hunting Algorithm

        High-Level Description:
        We determine if our reputation is correlated to our utility each round.
        If there is a positive correlation, then we want to hunt more often to increase our reputation and therefore our utility.
        If there is no correlation or a negative correlation, we slack, which is more likely to increase our utility while lowering our reputation.

        Step-By-Step Description:
        1. Add our current reputation to the end of the reputation history array. Pop the oldest value in the array.

        2. Are we in the early game?

        2a. Yes, so we gradually increase our likelihood of hunting to build a strong positive slope in our reputation.

        2b. No, we set our likelihood of hunting equal to the correlation coefficient scaled by the correlation significance.
            NOTE: If the correlation coefficient is less or equal to 0, there is no chance of hunting, as random() is in the interval (0,1]

        3. If we are not in the early game, enable "nice" edge detection.
            "NICE" EDGE DETECTION: Hunt with players with very high reputations, and Slack with players with very low reputations.

        4. Calculate a random number for each player, if that number is less than out likelihood of hunting, we hunt.

        5. Return the list of decisions.

        """
        hunt_decisions = list()

        # Remove the oldest element from the Self-Reputation History List        
        self.repArr.pop(0)
        # Append Current reputation to Self-Reputation History List
        self.repArr.append(current_reputation)


        # Likelihood of hunting this round (determined later)
        huntTest = 0.0

        # In the initial rounds, 
        if round_number <= self.history:
            # We need to build up a good history before using the correlation
            huntTest = (1.0/self.history) * round_number
        else:
            # Use Coefficient
            huntTest = self.corrcoef[0] * (1-self.corrcoef[1]) # Between -1 and 1, we want a positive correlation in order to hunt



        # Okay, actually create the hunt decisions list

        for x in player_reputations:
            # Edge Test after completing test rounds
            if round_number > self.history:
                if x < self.edges:
                    huntTest = 0
                elif x > (1-self.edges):
                    huntTest = 1
            if huntTest > self.random.random():
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        """
        Self-Reputation / Utility Correlation Hunting Algorithm Continued

        6. Calculate our total utility for the round and add it to the Utility History Array. 
        """

        # Pop the oldest utility from Utility History Array
        self.utilArr.pop(0)
        # Append Current utility to Utility History Array
        self.utilArr.append(sum(food_earnings))



    def round_end(self, award, m, number_hunters):
        """
        Self-Reputation / Utility Correlation Hunting Algorithm Continued

        7?. Add the public goods to this round's utility.
            NOTE: We tried testing with and without this feature, and the algorithm performed better without it.

        7. Calculate the correlation coefficient and significance between the most recent rounds' utility and self-reputation.
            This is used for next round's likelihood of hunting.
        """

        # Add award to appended utility, recalculate coefficient of correlation
        # self.utilArr[len(self.utilArr)-1] += award ### NAH, don't worry about the public goods right now...

        # Recalculate coefficient of correlation
        self.corrcoef = self.scipy.stats.pearsonr(self.repArr, self.utilArr)
