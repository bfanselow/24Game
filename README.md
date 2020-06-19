# 24Game
Play and/or generate games for the Math "24" Game

Background on the game: https://en.wikipedia.org/wiki/24_Game

#### TODO: Put a UI around this code and create a challenge to solve 10 games in shortest amount of time

---

### Play a single game (possible that solutions do not exist!)
#### You can hide the solutions, but we show them in this example. 
```
>>> from twenty_four_game import build_game
>>> build_game()
{'numbers': [2, 5, 8, 2], 'solutions': ['(2*(5+8))-2', '(2*(8+5))-2', '((5+8)*2)-2', '((8+5)*2)-2']}

game = build_game()
numbers = game['numbers']
solution_list = game['solutions']
print("NUMBERS: %s" % (numbers))
print("SOLUTIONS: %d" % len(solution_list))
for i,s in enumerate(solution_list, start=1):
    print("%d: %s" % (i,str(s)))
...
```

### Play or build multiple games (ALL with one or more solutions)
```
>>> from twenty_four_game import generate_valid_games
>>> generate_valid_games(2)
[{'numbers': [4, 6, 9, 6], 'solutions': ['(4*9)-(6+6)', '((4*9)-6)-6', '((6-4)*9)+6', '6-((4-6)*9)', '(6*(9-4))-6', '6+((6-4)*9)', '((9-4)*6)-6', '(9*4)-(6+6)', '((9*4)-6)-6', '(9*(6-4))+6']}, {'numbers': [2, 1, 5, 3], 'solutions': ['((2+1)+5)*3', '(2+(1+5))*3', '(2+1)*(5+3)', '(2+1)*(3+5)', '((2+5)+1)*3', '(2+(5+1))*3', '(2*(5-1))*3', '2*((5-1)*3)', '((2+3)*5)-1', '(2*3)*(5-1)', '((1+2)+5)*3', '(1+(2+5))*3', '(1+2)*(5+3)', '(1+2)*(3+5)', '((1+5)+2)*3', '(1+(5+2))*3', '((5+2)+1)*3', '(5+(2+1))*3', '(5*(2+3))-1', '((5+1)+2)*3', '(5+(1+2))*3', '((5-1)*2)*3', '(5-1)*(2*3)', '((5-1)*3)*2', '(5-1)*(3*2)', '(5+3)*(2+1)', '(5*(3+2))-1', '(5+3)*(1+2)', '3*((2+1)+5)', '((3+2)*5)-1', '3*((2+5)+1)', '(3*2)*(5-1)', '3*((1+2)+5)', '3*((1+5)+2)', '(3+5)*(2+1)', '3*((5+2)+1)', '(3+5)*(1+2)', '3*((5+1)+2)', '(3*(5-1))*2', '3*((5-1)*2)']}]

games = generate_valid_games(5)
for game in games:
    solution_list = game['solutions']
    numbers = game['numbers']
    print("NUMBERS: %s" % (numbers))
    print("SOLUTIONS: %d" % len(solution_list))
    for i,s in enumerate(solution_list, start=1):
        print("%d: %s" % (i,str(s)))
    print("\n")
...
```

##### Set DEBUG flag in the script to change verbosity level
