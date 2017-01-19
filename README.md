# Asteroid Attack!

A simple Pygame learning project. 

# Video

[Video!](https://www.youtube.com/watch?v=qiWfpnrnH_w "Asteroid Attack")

# Features

* Simple, intuitive UI
* Two game modes:
  * Campaign: Battle through 8 levels and try to gt a highscore
  * Simulator: Test your skills by creating your own level
* Lots of different powerups and enemies
* Persistent local highscores

# Installation notes

Requires Python 3 and Pygame. Creates and edits a highscores file (asteroid-attack-program-highscores.p) in the same folder as asteroid_attack.py so keep it in it's own directory to prevent it from interfering with anything else.   

# Change log

* 19/01/2017
  * Boss battles have arrived! Test yourself in battle against two bosses with various unique and increasingly difficult mechanics. Boss battles occur mid way through the campaign and in the final level.
  * Game no longer crashes when adding a new highscore.
* 14/01/2017
  * Local multiplayer support! Plug in a controller and navigate the asteroid field with a friend. Be wary though, as bullets from a friend can damage your ship, and you have one less life in multiplayer to keep things balanced.
  * Separate high-scores for single and multiplayer. To support this, the high-scores screen now has a tabbed display.
  * There is now a small sound effect when hovering over buttons.
* 18/12/2016
  * Added strong purple asteroids. These are slow, but take multiple shots to destroy and will cause some hefty damage if you collide with one. All levels have been reworked to make room for the newly added enemies, with different obstacles now appearing in earlier levels. Finally, the code handling collision detection, death etc. has been given a significant rewrite to reduce unneeded code repetition and make it easier to add new enemies in the future.
* 13/12/2016
  * Added fragmenting asteroids. These can be found in level 8.
* 09/12/2016
  * Added simple ship appearance customisation options that work in both game modes.
* 07/12/2016
  * Added sound effects to indicate the player is coming to the end of a level. "Level complete" screens are again being correctly displayed after each level.
