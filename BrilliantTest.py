#!/usr/local/bin/python

import ConfigParser
import BrilliantUtil
import inspect
import random

class TribesMan:

	def __init__(self, module, algorithm):
		
		# Play Data
		self.module = module
		self.algorithm = algorithm
		
		# Metrics
		self.food = 0.0
		self.hunts = 0.0
		self.slacks = 0.0
		
		# Game End Round
		self.gameOver = -1

	def addFood(self, amount, roundNum):
		self.food += amount
		if self.food < 1:
			self.gameOver = roundNum
		else:
			self.gameOver = -1

	def getReputation(self):
		if self.hunts + self.slacks == 0:
			return 0
		return self.hunts / (self.hunts + self.slacks)

	def hunt(self):
		self.hunts += 1
	def slack(self):
		self.slacks += 1


class HungerGames:
	def __init__(self, minRounds, endProb, tribesMen):
		"""
		Should be a list of tribesmen to compete against each other.
		"""
		print("Initializing New Game...")
		print("Number of Players: " + str(len(tribesMen)))
		print("Minimum Rounds: " + str(minRounds))
		print("Increase in chance of ending after each round: " + str(1-endProb))
		print("\n")
		print("NOTE: We do not take the time to randomize hunting interactions.\n\tRemember that tracking interactions won't work in the actual game.")
		print("\n")


		self.t = minRounds
		self.r = endProb

		self.round = 1
		self.end = 0

		self.p = len(tribesMen)
		self.players = tribesMen
		self.deadPlayers = list()

		# Divy out initial food rations
		for player in self.players:
			player.addFood(300 * (self.p-1), 1)

	def CheckEndConditions(self):
		if self.p < 2:
			return False
		else:
			if self.round < self.t:
				return True
			else:
				if random.random() < self.end:
					return False
				else:
					self.end = 1 - (self.r**(self.round - self.t))
					return True

	def run(self):

		# Check Ending Conditions
		while self.CheckEndConditions():

			# print("Starting round: " + str(self.round))

			# Create Reputation List
			repList = [x.getReputation() for x in self.players]

			# Set Random public goods number
			m = round(random.random() * self.p * (self.p-1))

			# Generate results matrix
			results = list()
			for x in range(self.p):
				currentRep = repList[x]
				del repList[x]
				row = self.players[x].module.hunt_choices(self.round, self.players[x].food, self.players[x].getReputation(), m, repList)
				repList.insert(x, currentRep)
				row.insert(x, '\a')
				results.append(row)
			# Update Reputations

			hunt_tracker = 0

			for row in range(self.p):
				for col in range(self.p):
					if results[row][col] == 'h':
						self.players[row].hunt()
						hunt_tracker += 1
					elif not results[row][col] == '\a':
						self.players[row].slack()

			# Generate Food Earnings
			for row in range(self.p):
				food_earnings = list()
				for col in range(self.p):
					if row == col:
						pass
					else:

						#         Opponent                     Player
						if   results[col][row] == 'h' and results[row][col] == 'h':
							# Both Hunted, no food reward
							food_earnings.append(0)
						elif results[col][row] == 'h' and results[row][col] == 's':
							# Slacked a hunt, food gain
							food_earnings.append(1)
						elif results[col][row] == 's' and results[row][col] == 'h':
							# Hunted a slacker, big food loss
							food_earnings.append(-3)
						elif results[col][row] == 's' and results[row][col] == 's':
							# Double slack, food loss
							food_earnings.append(-2)
				# Give player the chance to react to food earnings
				self.players[row].module.hunt_outcomes(food_earnings)
				# Update food amount for players
				self.players[row].addFood(sum(food_earnings), self.round)

			# Add public goods, if applicable
			if hunt_tracker >= m:
				award = 2 * (self.p-1)
			else:
				award = 0

			# Add food to each player
			for player in self.players:
				player.addFood(award, self.round)

			# Check for dead
			recentlyDead = list()
			for player in self.players:
				if player.gameOver > 0:
					recentlyDead.append(player)
					self.p -= 1
					print("Here lies a " + player.algorithm + " who died in round " + str(self.round) + ".")

			# Remove the bodies
			for player in recentlyDead:
				self.players.remove(player)
				self.deadPlayers.append(player)

			# For those remaining, signal the round end
			for player in self.players:
				player.module.round_end(award, m, self.p)

			# Increment Round Number
			self.round += 1

		# Print Results
		print("\n")
		print("Game Ended at round " + str(self.round) + ".")

		# Sort Players by remaining food
		self.players.sort(key=lambda x: x.food, reverse=True)

		for player in self.players:
			print(player.algorithm + ": " + str(player.food) + ", " + str(player.getReputation()))




def main():
	
	print("\n")

	# Parse Config File
	config = ConfigParser.ConfigParser()
	config.readfp(open('BrilliantTest.cfg'))

	# Read Global Config Options
	t = config.getint("global", "rounds")
	r = config.getfloat("global", "end_probability")

	# Create list of tribesmen
	tribesMen = list()
	print("Validating Algorithms...")
	for algorithm in config.options("algorithms"):
		algMod = BrilliantUtil.ImportAlgorithm(algorithm)

		# Check if is a valid module
		if not BrilliantUtil.Validate(algMod) == False:
			print("Succeeded in validating: " + algorithm)
			num = config.getint("algorithms", algorithm)

			# See if it is using the OOP Method
			c = BrilliantUtil.Validate(algMod)
			if inspect.isclass(c):

				# Add new instance of the class
				for x in range(num):
					tribesMen.append(TribesMan(c(), algorithm))

			else:

				# Add new Instances of the module
				for x in range(num):
					tribesMen.append(TribesMan(BrilliantUtil.ImportAlgorithm(algorithm), algorithm))
		else:
			print("Failed to validate: " + algorithm)

	print("\n\n")

	# At this point, we should have a full list of tribesmen in the tribesMen list
	game = HungerGames(t, r, tribesMen)
	game.run()


if __name__ == '__main__':
	main()
