"""
  File: 24game.py

  Description:
   This script generates problems and solutions for the "24" math game  (https://en.wikipedia.org/wiki/24_Game)

  Author: Bill Fanselow  2020-06-18

  Credit to "OregonTrail" on StackOverflow for ideas on simplifying the logic.
  (https://stackoverflow.com/questions/25028929/24-game-using-python/25029244)

  --------------
  Logic:
    Each round of play consists of four numbers and three operators.
    The four numbers can be arranged in 4!=24 ways (order matters).
    Since, operators can be repeated, there are 4**3=64 operator permutations.

    It might seem that we would have 24*64=1560 possible math equation permutations from
    combining the number-seq permuatations with the operator permutations.

    However, the actual number of mathematically-unique equations is much less than this
    due to many of the equations being mathematically equivelent as a result of
        the Commutitive and Associative properties of addition and multiplication:
         * Commutative: 2+3 = 3+2,  and 2*3 = 3*2
         * Associative: (2+4)+3 = 2+(4+3), and (2*3)*4 = 2*(3*4)


     After generating a random sequence of 4 numbers we perform all possible
     mathematical permuations (except those involving division-by-zero) to
     identify which ones result in 24.

  --------------
  NOTES:
  1) It is possible (though not ususally done) to arrive at a soltuion by dividing and
     multiplying numbers that are not evenly divisible.
     For example, given the numbers (4, 5, 6, 5):
       a) 4 / 5 = 0.8
       b) 6 * 5 = 30
       c) 30 * 0.8 = 24

  TODO: Need to validate why we have 128 mathematically unique calculations for each game.
        This number seems suspiciously low.

"""

import itertools
import random

DEBUG = 2

# Play the game with either 1-digit limit (1-9) or 2-digit limit (1-24)
DIGITS = 1

# All operators
op_list = [ '+', '-', '*', '/' ]

# Generate permuations of 3 operator sequences (with repeat), calculated by the Cartesion-product
ops_perms = list(itertools.product(op_list, repeat=3))

#-----------------------------------------------------------------------------------------
def dprint(lvl, msg, end=None):
    """ Print if at/above the DEBUG level"""
    if lvl <= DEBUG:
        print("(D%d): %s" % (lvl,msg), end=end)

#-----------------------------------------------------------------------------------------
def get_num_permutations(num_list):
    """
     Build a list of number permuations from passed 4-number num-list.
     Args: list containing 4 numbers.
     Returns: list of tuples, each tuple being an unique arrangemnt of the 4 numbers
    """
    num_perms = list(itertools.permutations(num_list))
    return num_perms

#-----------------------------------------------------------------------------------------
def check_24(ns_list, os_list):
  """
   Take a list of 4-digit tuples, and a list of 3-operator tuples, for example ('+' '*', '*')
   and determine if 24 can be made from any of the combined mathematical operations.
   Store all valid solutions.
   Args:
    * ns_list: list of number-sequence tuples, each containing uniq combo of 4 numbers
    * os_list: list of operator-sequence tuples, each containing uniq combo of 3 operators
   Return: list of valid solutions. Can be empty!

   TODO: The difference between the inner "for" loops can be abstracted away if prefix
   expressions are generated and evaluated instead.
  """

  token_set = []
  solutions = []
  solution_tokens = []

  tot_equations = 0

  # Iterate over list of number sequences
  for ns in ns_list: # example (3,3,2,2)

    # Iterate over operators, for sequential operations: example below for ns=(3,3,2,2)
    for op in os_list:
        tot_equations += 1
        result = calc(ns[0], op[0], ns[1])    # 3+3=6
        result = calc(result, op[1], ns[2])   # 6*2=12
        result = calc(result, op[2], ns[3])   # 12*2=24
        if result == 24:
            sol = "((%d%s%d)%s%d)%s%d" % ( ns[0], op[0], ns[1], op[1], ns[2], op[2], ns[3] )
            token_set = (ns[0], op[0], ns[1], op[1], ns[2], op[2], ns[3] )
            dprint(1, ">>> Solution (seq): %s" % (sol) )
            solution_tokens.append( token_set )
            solutions.append( sol )

    # Iterate again over operators for paired operations: example below for ns=(8,4,1,1)
    for op in os_list:
        tot_equations += 1
        result1 = calc(ns[0], op[0], ns[1]) # (8+4)=12
        result2 = calc(ns[2], op[1], ns[3]) # (1+1)=2

        # pass on any divide-by-zero options
        if op[2] == '/' and result2 == 0:
            dprint(4, ">>> Ignore div-by-zero: (%d/%d) " % (result1, result2) )
            continue

        result = calc(result1, op[2], result2) # (12*2)=24
        if result == 24:
            sol = "(%d%s%d)%s(%d%s%d)" % ( ns[0], op[0], ns[1], op[2], ns[2], op[1], ns[3] )
            token_set = (ns[0], op[0], ns[1], op[2], ns[2], op[1], ns[3] )
            if token_set in solution_tokens:
               dprint(2, ">>> Non-Unique Solution (pair): %s" % (sol) )
               continue
            dprint(1, ">>> Solution (pair): %s" % (sol) )
            solutions.append( sol )

    dprint(4, "Total-equations: %d" % (tot_equations))
    return solutions


#-----------------------------------------------------------------------------------------
def calc (n1, op, n2):
    """
    Calculate the mathematical expression given be two numbers (n1, n2) and an operator (op).
    TODO: this function can be avoided by using Python's "op" module, and generating permutations of
    function references rather than "op" strings
    """
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        return n1 / n2

#-----------------------------------------------------------------------------------------
def get_random_four():
    """
     Generatate set of 4 random numbers.
     If DIGITS=1, range is 1-9
     If DIGITS=2, range is 1-24
     Return: list of 4 numbers
    """
    random_four = []
    for i in range(0,4):
        if DIGITS == 2:
            n = random.randint(1,24)
        else:
            n = random.randint(1,9)
        random_four.append(n)
    return random_four

#-----------------------------------------------------------------------------------------
def build_game():
    """
    Create a random sequence of 4 numbers and find solutions
    """
    r4 = get_random_four()
    number_sequences = get_num_permutations(r4)

    dprint(4, "NS: %s" % number_sequences)
    dprint(4, "OPS (%d): %s" % (len(ops_perms), ops_perms), end="\n\n")

    solution_list = check_24(number_sequences, ops_perms)

    result = {
     'numbers': r4,
     'solutions': solution_list
    }

    return result

#-----------------------------------------------------------------------------------------
def generate_valid_games(N):
    """
     Create a set of N "games" which have one or more solutions.
     Args: (int) number of "games" to create.
     Return the number-sequences and corresponding solutions for each.
    """

    games = []
    while len(games) <= N:
        game = build_game()
        N_solutions = len(game['solutions'])
        if N_solutions:
            games.append(game)

    return games

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':

    ## Perfom a single game
    game = build_game()
    numbers = game['numbers']
    solution_list = game['solutions']
    print("NUMBERS: %s" % (numbers))
    print("SOLUTIONS: %d" % len(solution_list))
    for i,s in enumerate(solution_list, start=1):
        print("%d: %s" % (i,str(s)))


    print("\n------------------------\n")

    ## Perform 5 (valid) games!
    games = generate_valid_games(5)
    for game in games:
        solution_list = game['solutions']
        numbers = game['numbers']
        print("NUMBERS: %s" % (numbers))
        print("SOLUTIONS: %d" % len(solution_list))
        for i,s in enumerate(solution_list, start=1):
            print("%d: %s" % (i,str(s)))
        print("\n")
