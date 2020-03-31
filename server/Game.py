#!/usr/bin/python3

import random
import string
import json

class Game(object):
	"""	
		Game: Initialize with number of players (2-4): 
			g = Game(number_of_players)

		2 players: levels 1-12, 2 lives, 1 throwing star
		3 players: levels 1-10, 3 lives, 1 throwing star
		4 players: levels 1-8,  4 lives, 1 throwing star
	"""
	def __init__(self, number_of_players):
		if (not 2 <= number_of_players <= 4):
			raise ValueError("Number of players must be between 2 and 4.\nExample: g = Game(4)")

		self.id = "".join( random.sample(string.ascii_uppercase, 4) )
		self.players = number_of_players
		self.deck = list( range(1,101) )
		self.lives = number_of_players
		self.stars = 1
		self.levels = [12,10,8][number_of_players-2]
		self.position = 0
		self.level = 1
		self.blind = False
		self.hands = [[] for i in range(number_of_players)]
		self.pile = []
		self.discard = []
		self.result = 0

		self.dealHands()

	def getId(self):
		return self.id

	def addStar(self):
		""" The team can posess a maximum of 3 throwing stars """
		if (self.stars < 3):
			self.stars = self.stars + 1
		return self.stars

	def addLife(self):
		""" The team can posess a maximum of 5 lives """
		if (self.lives < 5):
			self.lives = self.lives + 1
		else:
			return self.lives

	def playStar(self):
		""" 
		At any point during a level a player can suggest that a throwing star be played
		- this is signalled by raising a hand. If all the players agree, the throwing star 
		is deployed and each player discards the lowest card in their hand by placing it 
		face up to one side. One throwing star is then set aside. 

		Next, all the players refocus and the game continues. 
		"""
		if (self.stars >= 1):
			self.stars = self.stars - 1
			self._discardLowestInEachHand()
			return self.stars
		else:
			return False

	def refocus(self):
		pass	 

	def loseLife(self):
		if self.lives > 1:
			self.lives = self.lives - 1
		else:
			gameOver(2)

		return self.lives

	def gameOver(self, num):
		self.result = num

	def nextLevel(self):
		"""
		There are rewards for completing levels 2,3,5,6,8,9 - alternate star, life
		If the team successfully completes all the levels in the stack 
		(and is dancing joyfully on cloud nine), play goes on immediately in blind mode.

		The team starts again at level 1 with all its remaining lives and throwing stars, 
		but this time all the cards are played face down on the deck in the centre of the table. 
		At the end of the level this stack is turned over and the sequence of cards is checked.

		If a player has made a mistake, this costs one life. The remaining rules are unchanged. 
		How many levels can the team complete blind?

		"""

		if self.result == 2: 
			return False

		next_level = self.level + 1

		if (not self.blind):
			# Rewards
			if (self.level in [2,5,8]):
				self.addStar()
			elif (self.level in [3,6,9]):
				self.addLife()

			if (1 <= next_level <= self.levels):
				self.level = next_level;
			else:
				# The players have moved on to blind mode
				self.blind = True
				self.level = 1

		# In Blind Mode, so level limit is 100 / self.players
		else: 
			if next_level < (100 / self.players):
				self.level = next_level
			else:
				gameOver(1)
				return False
		
		self.dealHands()
		return self.level

	def printStateJSON(self):
		cs = {
			"id": self.id,
			"players": self.players,
			"lives": self.lives,
			"stars": self.stars,
			"levels": self.levels,
			"level": self.level,
			"blind": self.blind,
			"discard" : self.discard,
			"pile" : self.pile,
			"hands" : self.hands
		}

		print(json.dumps(cs))


	def nextHand(self):
		"""
		In the first round (level 1) each player receives 1 card, 
		in the second round (level 2) they receive 2 cards, and so on. 
		"""
		start = self.position
		end = self.position + self.level

		if ( end <= len(self.deck) ):
			self.position = end
			return self.deck[start:end]
		else:
			return False
	

	def dealHands(self):
		random.shuffle(self.deck)
		self.position = 0
		for i in range(self.players):
			cards = self.nextHand()
			if cards:
				self.hands[i] = sorted(cards)
			else:
				return False
				self.gameOver()

		return True

	def playCard(self, idx):
		if len(self.hands[idx]) > 0:	
			card = min(self.hands[idx])

			if card > self._lowestCard():
				self.loseLife()
				self._discardLower(card)
				self.discard.append( self.hands[idx].pop(0) )
				return False
			else:
				self.pile.append( self.hands[idx].pop(0) )
				if self._allHandsEmpty():
					self.nextLevel()
				return True
		else:
			return False

	def _lowestCard(self):
		hl = []
		for hand in self.hands:
			hl += hand
		return min(hl)

	def getHand(self, idx):
		return self.hands[idx]

	def _discardLower(self, value):
		print("discard lower:", value, len(self.hands))
		for i in range(len(self.hands)):
			for j in range(len(self.hands[i])):
				if self.hands[i][j] < value:
					self.discard.append( self.hands[i].pop(j) )
		if self._allHandsEmpty():
			self.nextLevel()

	def _discardLowestInEachHand(self):
		for i in range(len(self.hands)):
			if len(self.hands[i] == 0): 
				continue
			hand_min = min(self.hands[i])
			hand_min_idx = self.hands[i].index(hand_min)
			self.discard.append( self.hands[i].pop(hand_min_idx) )

	def _allHandsEmpty(self):
		count = 0
		for hand in self.hands:
			if len(hand) == 0:
				count = count + 1
		if count == self.players:
			return True
		return False

# from Game import Game
# g = Game(4)
# g.state()
# g.playCard(0)
# g.state()
# g.playCard(0)
# g.state()
