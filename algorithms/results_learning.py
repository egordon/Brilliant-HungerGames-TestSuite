

class Player:
    def __init__(self):
        """
        Initialize all arrays and set magic numbers.
        NOTE: All "magic" numbers were calibrated using a self-programmed testing suite.
        """

        ### MAGIC NUMBERS ###

        # Used for "nice" edge detection.
        # If reputation is greater than 1-edges, we hunt
        # If reputation is less than edges, we slack
        self.edges = .1

        # Base for the exponent to scale the hunt and slack chance
        self.expBase = 2.0

        ### END MAGIC NUMBERS ###

        # Initialize Hutn and Slack chance for 50/50
        self.huntChance = 0.5
        self.slackChance = 0.5
        self.totalChance = self.huntChance + self.slackChance

        # Initialize Modules
        self.random = __import__("random")


    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):
        hunt_decisions = list()
        huntTest = 0.0

        # Set the likelihood of hunting to the normalized hunt chance.
        huntTest = self.huntChance / self.totalChance

        # Okay, actually create the hunt decisions list

        for x in player_reputations:
            # Edge Test after first round
            if round_number > 1:
                if x < self.edges:
                    huntTest = 0.0
                elif x > (1-self.edges):
                    huntTest = 1.0
            if huntTest > self.random.random():
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        slackUtility = 0.0
        huntUtility = 0.0

        for x in food_earnings:
            if x == 1:
                slackUtility += 1.0
            elif x == -2:
                slackUtility -= 2.0
            elif x == -3:
                huntUtility -= 3.0

        self.huntChance *= self.expBase ** huntUtility
        self.slackChance *= self.expBase ** slackUtility

        self.totalChance = self.huntChance + self.slackChance

        # Normalize
        self.huntChance = self.huntChance / self.totalChance
        self.slackChance = self.slackChance / self.totalChance
        self.totalChance = self.huntChance + self.slackChance


    def round_end(self, award, m, number_hunters):
        pass
