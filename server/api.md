
# Ordinal Game API

## Overview
The first two possible actions a user could take are:
* create a new game
* join an existing game

When you create a new game, you also create a new player. The API responds with the `game_id` and the `player_id`, and sets a cookie for the `game_id` and `player_id`. There is no other way to retrieve these ids later on, so be sure to save this information.

```{'player_id': 'DGQIWAHOLE', 'game_id': 'RPZL'}```

Next, POST the provided ids in order to retreive the game state:
```
{
	"action" 	: "getstate",
	"player_id"	: "ABCDEFGHIJK",
	"game_id"	: "ABCD"
}
```
The API responds with the current details of the game, including the player's hand:
```
{"stars": 1, "result": 0, "discard": [], "lives": 2, "players": 2, "blind": false, "levels": 12, "pile": [], "player_id": "DGQIWAHOLE", "level": 1, "state_id": 1586364460.762625, "hand": [90], "game_id": "RPZL"}
```
Whenever the client requests a "play" action (`playcard` or `playstar`), the `state_id` is needed to ensure that 

## action

* `new`
	* starts a new game 
	* requires a `name` and number of `players`
* `join`
	* adds a player to an existing game
	* requires `game_id` and `name`
* `getstate`
	* requests the current game state
	* requires `game_id` and `player_id`
* `playcard`
	* asks the server to play the lowest card for `player_id`
	* requires `player_id` , `game_id`, and the latest `state_id`
* `playstar`
	* asks the server to play a star
	* requires `player_id` , `game_id`, and the latest `state_id`

### new
Starts a new game and adds the first player.
```
{
	"action" 	: "new",
	"name"		: "BabyBoo",
	"players"	: 3
}
```
#### Required values
`players` 
Accepted values are 2,3, or 4

`name` 
string where length < 255

### getstate
Returns the game state, including the cards/hand for a given player.
```
{
	"action" 	: "getstate",
	"player_id"	: "ABCDEFGHIJK",
	"game_id"	: "ABCD"
}
```
#### Required values
`player_id` 
this id is returned from the server when starting a new game or creating a new player. It is also set as a cookie on the client browser.

`game_id` 
this id is returned from the server when a new game is created.
