
# Ordinal Game API

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