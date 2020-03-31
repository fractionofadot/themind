#!/usr/bin/python3

import os
import cgi
import json
import string
import random
import pickle

from Game import Game

PlayerDB = []
GameDB = []

def main():
	# Each record consists of id, ip_addr, and name
	PlayerDB = loadPlayerDB()

	# Each record consists of an ID and a Game() object
	GameDB = loadGameDB()

	try:
		remote_ip = cgi.escape( os.environ['REMOTE_ADDR'] )
	except:
		remote_ip = None

	pid = getPlayerId()

	jsonHeader()

def identifyUser():
	pass

def loadPlayerDB():
	return []

def loadGameDB():
	gdb_file_path = "gdb"

	try:
		with open(gdb_file_path, "rb") as f:
			return pickle.load(f)
	except FileNotFoundError:
		with open(gdb_file_path, "wb") as f:
			pickle.dump([], f)
		return []

def sendError(msg):
	print( json.dumps({"error" : msg}) )

def performAction():
	form = cgi.FieldStorage()

	action = form.getfirst("action", None)
	game_id = form.getfirst("game", None)
	players = form.getfirst("players", None)
	name = form.getfirst("name", None)

	if not (2 <= players <= 4):
		sendError("Invalid value for players. Valid values are 2-4")

	if game_id:
		if not any(game_id in row for row in GameDB):
			sendError("No game found with that ID")
			return False

	game = GameDB[game_id]

	valid_actions = ["playCard", "newGame", "playStar", "getState", "joinGame"]

	if action == "newGame":
		newGame()
	elif action == "joinGame":
		joinGame(game)
	elif action == "playCard":
		playCard(game)
	elif action == "playStar":
		playStar(game)
	elif action == "getState":
		getState(game)
	else:
		print(json.dumps({"error":'A valid action must be specified: {}'.format(valid_actions)}))
		return False

def newGame(number_of_players, name):
	game = Game(number_of_players)
	GameDB.append({
		str(game.id) : game
	})

	jsonHeader()
	game.printStateJSON()

def getState(game):
	game.printStateJSON()

def playCard(game, player):
	result = game.playCard(player)
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