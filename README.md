# 24Game
Play and/or generate games for the Math "24" Game

Background on the game: https://en.wikipedia.org/wiki/24_Game


### Play a single game
#### You can hide the solutions, but we show them in this example. NOTE: There may or may not be solutions!
```
from 24game import build_game
...
game = build_game()
numbers = game['numbers']
solution_list = game['solutions']
print("NUMBERS: %s" % (numbers))
print("SOLUTIONS: %d" % len(solution_list))
for i,s in enumerate(solution_list, start=1):
    print("%d: %s" % (i,str(s)))
```

### Play or build a multiple games (ALL with one or more solutions)
```
from 24game import generate_valid_games
...
#Perform 5 (valid) games
games = generate_valid_games(5)
for game in games:
    solution_list = game['solutions']
    numbers = game['numbers']
    print("NUMBERS: %s" % (numbers))
    print("SOLUTIONS: %d" % len(solution_list))
    for i,s in enumerate(solution_list, start=1):
        print("%d: %s" % (i,str(s)))
    print("\n")
```

##### Set DEBUG flag in the script to change verbosity level
