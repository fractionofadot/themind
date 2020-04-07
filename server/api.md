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
