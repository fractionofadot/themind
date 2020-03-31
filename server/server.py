#!/usr/bin/python3

import os
import cgi
import json
import string
import random
import pickle

from Game import Game

PlayerDB = {}
GameDB = {}

gdb_file_path = "db/gdb"
pdb_file_path = "db/pdb"

def main():
	# {id : pid, ip : ip_addr, name : name}
	PlayerDB = loadPlayerDB()

	# {id: Game() object}
	GameDB = loadGameDB()

	performAction()

def identifyUser():
	pass

def loadPlayerDB():
	return {}

def loadGameDB():
	try:
		with open(gdb_file_path, "rb") as f:
			return pickle.load(f)
	except FileNotFoundError:
		with open(gdb_file_path, "wb") as f:
			pickle.dump({}, f)
		return {}

def sendError(msg):
	jsonHeader()
	print( json.dumps({"error" : msg}) )

def performAction():
	form = cgi.FieldStorage()

	action = form.getfirst("action", None)
	game_id = form.getfirst("game", None)
	players = int(form.getfirst("players", 0))
	name = form.getfirst("name", None)

	game = None

	if game_id:
		if game_id not in GameDB.keys():
			sendError("No game found with that ID: {}".format(game_id))
			print(GameDB.keys())
			return False
		game = GameDB[game_id]
		

	valid_actions = ["playCard", "newGame", "playStar", "getState", "joinGame"]

	# START A NEW GAME
	if action == "newGame":
		if not (2 <= players <= 4):
			sendError("Invalid value for players. Valid values are 2-4")
			return False

		if not name:
			sendError("name is required to start a new game.")
			return False

		newGame(players, name)

	# JOIN A GAME	
	elif action == "joinGame":
		if game:
			joinGame(game)
		else:
			sendError("No game specified")
			return False

	# PLAY A CARD	
	elif action == "playCard":
		if game:
			playCard(game)
		else:
			sendError("No game specified")
			return False

	# PLAY A STAR CARD
	elif action == "playStar":
		if game:
			playStar(game)
		else:
			sendError("No game specified")
			return False

	# GET THE GAME STATE
	elif action == "getState":
		if game:
			getState(game)

	else:
		sendError('A valid action must be specified: {}'.format(", ".join(valid_actions) ) )
		return False

def newGame(number_of_players, name):
	game = Game(number_of_players)
	GameDB[game.id] = game

	with open(gdb_file_path, "wb") as file:
		pickle.dump(GameDB, file)

	jsonHeader()
	game.printStateJSON()
	print(GameDB.keys())

def getState(game):
	jsonHeader()
	game.printStateJSON()

def playCard(game, player):
	result = game.playCard(player)
	jsonHeader()
	game.printStateJSON()
	return result

def playStar():
	pass

def joinGame():
	pass

def jsonHeader():
	print("Content-type: application/json")
	print("")

def getPlayerId():
	if 'HTTP_COOKIE' in os.environ:
		cookie = cgi.escape( os.environ['HTTP_COOKIE'] )
		pid = split(cookie, '=')[1]
		return pid
	else:
		return setPlayerId()

def setPlayerId():
	pid = generatePid()

	while any(pid in row for row in PlayerDB):
		pid = generatePid()

	print( "Set-Cookie: id={}".format(pid) )
	return pid

def generatePid():
	return "".join( random.sample(string.ascii_uppercase, 10) )

main()