# roll20_quick_terrain
Simple GUI terrain generator appropriate for outdoor battle maps for tabletop roleplaying games played in Roll20.

## Requirements

* Python 3.x (for the GUI/generator)
* Access to the [Roll20 development server](https://app.roll20dev.net/), usually through a subscription (for using the terrain in your game)

## Usage

**!setup will delete all tokens on the map layer of the page the players are currently on.**

Checkout the screenshots ss1.png and ss2.png to see what stuff looks like.

### Setting up Roll20

* Upload the included image files into your Roll20 image library.
* Have a game set up on the Roll20 development server. Open up the scripts page for that game. Copy and paste the code from quick_interface.js into a new script, name it whatever you like.
* Hit "Save Script".
* *The URLs for the images at the top of the script will be wrong* (I haven't looked up/implemented how to get them automatically yet). As a workaround, in the map layer of the active player page in your Roll20 game, drag the images on to the board (creating a token for each one). 
  * Double click on each one and give them names you will recognize. In the chat box, enter the command !setup, and the tokens should be deleted. 
  * In the log on the Roll20 scripts page, you should see these names and some corresponding URLs. Change the word 'max' to 'thumb' at the end of each URL, and replace the appropriate URL in the STONE_IMAGE, PINE_IMAGE, etc. variables at the top of the script (URL must be in quotes).
* Hit "Save Script". You can now proceed with map generation and expect your maps to actually work!

### Generating maps
Run roll20TerrainGen.py. Play around with the sliders and hit Generate until you find something you like! *Note: not all relevant settings are in the GUI yet, you can edit the map size directly in the script under default_settings, and you can add different terrain types in main().*

### Getting your new terrain into Roll20

Copy (click the text, press Ctrl+A, then Ctrl+C) and paste (Ctrl+V) the output in the generator into the chatbox on Roll20 (starts with !setup). **All tokens on the map layer of the current player page will be deleted.** New tokens will be created on the map layer of the current player page to match the preview from roll20TerrainGen.py.

## License and Attribution

Copyright (C) 2016 Adam Mansfield

See LICENSE.txt for license details.

stone-pile.png by [Delapouite](http://delapouite.com/) under [CC by 3.0](https://creativecommons.org/licenses/by/3.0/).

pine-tree.png and wave-crest.png by [Lorc](http://lorcblog.blogspot.com/) under [CC by 3.0](https://creativecommons.org/licenses/by/3.0/).
