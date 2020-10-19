# A simple Python interface for zyngapoker.com
Do you want to cheat at online poker? Well do I have a package for you. Using this simple library you
can extract the internal game state of the [zyngapoker.com](zyngapoker.com) and then build a bot of your own.
I will be honest, installation is a bit meh. The code it self is kind of ugly. The end points that 
it exposes are kind of cool however. 

## Installation
1) Copy all of the code
2) Make sure that you can run `selenium` with chrome webdriver
3) Install `mitmproxy`

## How to use
Current version does not support automatic inputs, work in progress. So the ideal workflow is as follows

First step is to start the proxy server, open the Chrome browser and navigate to [zyngapoker.com](zyngapoker.com).

`python main.py`

Once you are logged and at the game table run 

`start_game()`

in the console. If you got this far then you have successfully connected to the interface. 

Since this is just a proof of concept package I did not bother implementing a smart way to dump data from the 
proxy server into the Python script so I am simply writing and reading the `wss.out` text file. 

## The main functions/properties
Players are placed around the table, each position(sit) is marked between 0 and 4, so 5 players max.
Find the number of chips currently in the pot. Int, default is `None`.
```python
IN: G.pot_size
```
```shell
OUT: 10000
```
To find whether it is the end of the match. Bool, default is `None`, once `None` was set to either `True` or `False` it should not go back to `None`.
```python
IN: G.match_end
```
```shell
OUT: False
```

To find the winning sit. Int, default is `None`. The variable obtains an integer value only when `G.match_end` is `True`.
```python
IN: G.who_won
```
```shell
OUT: 0
```

To find which stage of the card reveal. Int, default is `None`. This variable takes 4 possible values. 0 -- no cards, 1 -- flop, 2 -- street, 3 -- river.
```python
IN: G.card_reveal_stage
```
```shell
OUT: 3
```

To find cards on the table. List of dictionaries, default `None`. Once `None` was set to a list empty table is represented by an empty list `[]`. Each card is an unique entry in the list. Each card is represented by a dictionary, for example Ace of spades is `{"value":13,"suit":2}`. Cards are labled 2, 3, 4, 5, 6, 7, 8, 9, 10, 10(J), 11(Q), 12(K), 13(A); 0(Diamonds), 1(Hearts), 2(Spades), 3(Clubs).
```python
IN: G.cards_on_table
```
```shell
OUT: [{'value': 11, 'suit': 3}, {'value': 6, 'suit': 1}, {'value': 12, 'suit': 2}]
```

To find final cards of all players. Unless `G.match_end` is `True` variable has the `None` value. I think there is an issue as cards are only displayed when more than one person went `all in`.
```python
IN: G.final_cards
```
```shell
OUT: [{'sit': '1', 'card1': '14', 'suit1': '1', 'card2': '13', 'suit2': '0'}, {'sit': '4', 'card1': '14', 'suit1': '2', 'card2': '10', 'suit2': '3'}]
```

To look at the state of all players. Dictionary of dictionaries, default is `{'self':False,
              'active':False,
              'name':'',
              'folded':False,
              'raised-hist':[],
              'chips':-1,
              'checked':False,
              'called':False,
              'all-in':-1,
              'xp':-1,
              'empty-sit':True,
              'active-turn':False,
              'big-blind':None,
              'small-blind':None,
              'sel-option':None}`. Each key in the dictionary represents a sit at the table. `self` is boolean is `True` when that sit is player, `False` otherwise. `active` is `False` when player just joined then changed to `True`. `folded` is `True` when player folded their cards, `False` otherwise. `raised-hist` is a list that stores a history of raise amounts for that player. `chips` is an integer and shows how many chips is held at that sit, when `-1` means that no player is present. `checked` is `True` when player has checked on their turn. `called` is `True` when player calls, `False` otherwise. `all-in` shows the amount that player is put at stake, `-1` means that player did not go all in. `xp` probably is not experience but I am not sure what it is. `empty-sit` is `True` when not player player is present at the sit, `False` otherwise. `active-turn` is `True` when it is that sits turn. `big-blind` is the amount (integer) placed at the big blind, `None` is the default. `small-blind` similar to `big-blind`. `sel-option` is a string and it can take values `folded`,`raised`,`checked`,`called`,`all-in`; `None` is the default when player had not made any choice.
```python
IN: G.players
```
```shell
OUT: {0: {'self': False, 'active': True, 'name': '', 'folded': False, 'raised-hist': [200000], 'chips': 7602873, 'checked': False, 'called': False, 'all-in': -1, 'xp': 23735744, 'empty-sit': False, 'active-turn': False, 'big-blind': None, 'small-blind': None, 'sel-option': None}, 1: {'self': False, 'active': True, 'name': '', 'folded': False, 'raised-hist': [20000, 40000, 40000], 'chips': 6408970, 'checked': False, 'called': False, 'all-in': -1, 'xp': 32904652, 'empty-sit': False, 'active-turn': False, 'big-blind': None, 'small-blind': None, 'sel-option': None}, 2: {'self': False, 'active': True, 'name': '', 'folded': False, 'raised-hist': [], 'chips': 640000, 'checked': False, 'called': False, 'all-in': -1, 'xp': 1340000, 'empty-sit': False, 'active-turn': True, 'big-blind': None, 'small-blind': None, 'sel-option': None}, 3: {'self': False, 'active': True, 'name': '', 'folded': False, 'raised-hist': [], 'chips': 3852961, 'checked': False, 'called': False, 'all-in': -1, 'xp': 0, 'empty-sit': False, 'active-turn': False, 'big-blind': None, 'small-blind': None, 'sel-option': None}, 4: {'self': False, 'active': True, 'name': '', 'folded': False, 'raised-hist': [], 'chips': 1840000, 'checked': False, 'called': False, 'all-in': -1, 'xp': 24225270, 'empty-sit': False, 'active-turn': False, 'big-blind': None, 'small-blind': None, 'sel-option': None}}
```
