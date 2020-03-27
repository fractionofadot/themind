#!/usr/bin/python3

import random
import string

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
		self.hands = [] * number_of_players

		random.shuffle(self.deck)

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
		if (self.stars > 1):
			self.stars = self.stars - 1
		else:
			self.stars = 0

		return self.stars


	def refocus(self):
		pass	 

	def loseLife(self):
		if self.lives > 1:
			self.lives = self.lives - 1
		else:
			gameOver()

		return self.lives

	def gameOver(self):
		pass

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
		if (not self.blind):
			if (self.level in [2,5,8]):
				self.addStar()
			elif (self.level in [3,6,9]):
				self.addLife()

			nextLevel = self.level + 1

			if (1 <= nextLevel <= self.levels):
				self.level = nextLevel;
				return self.level
			else:
				self.blind = True
				self.level = 1
				return self.level
		else:
			self.level = self.level + 1
			return self.level

	def printGameInfo(self):
		print("id: ", self.id) 
		print("players: ", self.players) 
		print("lives: ", self.lives)
		print("stars: ", self.stars)
		print("levels: ", self.levels)
		print("deck: ", self.deck)

	def dealNext(self):
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
	

g = Game(random.choice([2,3,4]))
g.printGameInfo()

for i in range(1,15):
	print( g.nextLevel(), g.blind, g.lives, g.stars )

