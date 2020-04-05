#!/usr/bin/python3

import os
import cgi
import json
import string
import random
import pickle

from Game import Game

class GameServer():
	def __init__(self):
		self.gdb_file_path = 'db/gdb'
		self.pdb_file_path = 'db/pdb'
		self.GameDB = self.loadGameDB()
		self.PlayerDB = self.loadPlayerDB()
		self.request = {}

		self.parseRequest()

	def loadGameDB(self):
		try:
			with open(self.gdb_file_path, "rb") as file:
				return pickle.load(file)

		# If the file does not exist, create and return an empty object
		except FileNotFoundError:
			with open(self.gdb_file_path, "wb") as file:
				pickle.dump({}, file)
			return {}

	def saveGameDB(self):
		with open(self.gdb_file_path, "wb") as file:
			pickle.dump(self.GameDB, file)

	def loadPlayerDB(self):
		try:
			with open(self.pdb_file_path, "rb") as file:
				return pickle.load(file)

		# If the file does not exist, create and return an empty object
		except FileNotFoundError:
			with open(self.pdb_file_path, "wb") as file:
				pickle.dump({}, file)
			return {}

	def savePlayerDB(self):
		with open(self.pdb_file_path, "wb") as file:
			pickle.dump(self.PlayerDB, file)

	def jsonHeader(self):
		print("Content-type: application/json")
		print("")

	def sendError(self, msg):
		self.jsonHeader()
		print( json.dumps({"error" : msg}) )

	def requires(self, requirements):
		for r in requirements:
			if not self.request[r]:
				return False
			return True

	def createNewPlayer(self, name, game_id):
		total_players = self.GameDB[game_id].player_count
		if len( self.playersInGame(game_id) ) < total_players:
			player_id = "".join( random.sample(string.ascii_uppercase, 10) )
			self.PlayerDB[player_id] = { 
		 		'name' : name,
		 		'game_id' : game_id
			}
			self.savePlayerDB()

			return True
		return False

	def playersInGame(self, game_id):
		player_list = []
		for player in self.PlayerDB:
			if self.PlayerDB[player]['game_id'] == game_id:
				player_list.append(player)
		return player_list

	def parseRequest(self):
		valid_requests = {
			'new' 		: self.newGame, 
			'join' 		: self.joinGame, 
			'playcard' 	: self.playCard, 
			'playstar' 	: self.playStar, 
			'getstate' 	: self.getState
		}

		form = cgi.FieldStorage()
		action = form.getfirst("action", "").lower()

		self.request = {
			'game_id' 	: form.getfirst("game_id", "").upper(),
			'players' 	: int(form.getfirst("players", 0)),
			'name' 		: form.getfirst("name", ""),
			'player_id' : form.getfirst("player_id", None),
			'state_id' 	: form.getfirst("state_id", None)
		}

		if action in valid_requests:
			valid_requests[action]()
		else:
			self.sendError("Invalid action")
		
	def getState(self):
		# request=state&game_id=ABCD&player_id=AdgDIsdfSDP
		if self.requires( ['game_id', 'player_id'] ):
			game_id = self.request['game_id']
			if game_id in self.GameDB:
				game = self.GameDB[game_id]
				game.printStateJSON()
			else:
				self.sendError("Game not found")
		else:
			self.sendError("getstate requires game_id and player_id")

	def newGame(self):
		# request=new&name=Bunburry&players=2
		if self.requires( ['name', 'players'] ):
			game = Game(self.request['players'])
			self.GameDB[game.id] = game
			self.saveGameDB()

			self.createNewPlayer(self.request['name'], game.id)

			game.printStateJSON()
		else:
			self.sendError("new requires name and players")

	def joinGame(self):
		# request=join&name=JooJoo&game_id=ABCD
		if self.requires( ['name', 'game_id'] ):
			game_id = self.request['game_id']
			name = self.request['name']
			if game_id in self.GameDB:
				if self.createNewPlayer(name, game_id):
					game = self.GameDB[game_id]
					game.printStateJSON()
				else:
					self.sendError( "Game {} is full.".format(game_id) )
			else:
				sendError("Game {} does not exist".format(game_id) )
		else:
			self.sendError("join requires name and game_id")

	def playCard(self):
		if self.requires( ['name', 'players'] ):
			print("Good")
		else:
			self.sendError("Does not meet requirements")

	def playStar(self):
		if self.requires( ['name', 'players'] ):
			print("Good")
		else:
			self.sendError("Does not meet requirements")
