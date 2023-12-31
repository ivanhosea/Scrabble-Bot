# Scrabble Bot
Scrabble game between player (you) and a bot, which tries to find the highest score move every turn that it can make.
## Video Demo
https://www.youtube.com/watch?v=9H5_QmZnbpo
## Data Structure
The data structure used for searching allowed words to be made is a combination of Suffix Tree & Trie. The main tree is a Suffix Tree, but for every valid suffix in the Suffix Tree, it has a value of another Trie that stores the remaining prefix backwards. For example, for the word "player", the suffix "yer" will store a trie of substring "alp". This means for the words "player", "lawyer", and "flyer", the suffix "yer" in the Suffix Tree will have a Trie that contains the words "alp", "wal", and "lf". This design does make search extremely fast, but it does use a lot of memory than if it just use an ordinary Trie. The Suffix Tree also contains the precomputed value of the word (without score modifiers) in each node where word exists. Suffix Tree & Trie are also compressed to reduce the memory usage.
## Font
The font that I use can be downloaded at https://fonts.google.com/specimen/Courier+Prime
## Getting Started
1. Install Python 3
2. Install pygame
    ```
    pip install pygame
    ```
3. You need to provide txt file containing the word dictionary & a font file.
4. Replace the dictionary & font in game.ini with your dictionary & font filenames.
5. To run the game:
    ```
    python scrabble.py
    ```
## Files
- game_button.py: class containing the design & functionality of button in the game (swap button, pass button).
- game.py: class containing the whole functionality of the game.
- scrabble.py: the main class that primarily functions for putting everything together to make the UI.
- location.py: class (more like a struct) containing variables that indicate the location in the game UI.
- score.py: class indicating the scoreboard.
- scrabble_statics.py: this file contains some static functionality of scrabble.
- pygame_constants.py: this file contains the color codes and fonts for Pygame UI design.
- squares.py: class contains each component of the square in the board and rack (if they're empty, what kind of modifier they possess, etc).
- tile.py: class contains the design & functionality of the actual letter tile.
- tiles_deck.py: class contains the functionality of the deck of tiles (drawing, swapping, keeping track of what tiles is in the deck, etc).
- trie_node.py: contains the class of the Suffix Tree node that contains the 26 alphabet pointers to other nodes and a substring for compression and the value of the node, if the value is greater than 0, it means the word made from letters until that node exist.
- trie_leaf.py: almost the same as trie_node, but don't have node pointers to save memory.
- trie.py: the actual Suffix Tree class, when performing search, insert, and other Trie operations, this class is used.
- test_trie.py: not related to the game, but can be used to simulate the Suffix Tree, it can check if the word exist and what are the prefixes to the given suffix.
## Possible Improvements
- Add the blank tiles.
- Implement other algorithms (e.g., minimax), to make the bot be able to see multiple moves ahead.
- Save the Suffix Tree in other file format for faster load time during game start up.
- Make multiplayer LAN mode.
## References
- The World’s Fastest Scrabble Program: https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
- Coding the Perfect SCRABBLE Program: https://www.youtube.com/watch?v=d07ntA9W7YE