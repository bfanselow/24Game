"""
  File: 24game.py
  Description:
   This script generates problems and solutions for the "24" math game:
    (https://en.wikipedia.org/wiki/24_Game)

  Author: Bill Fanselow  2020-06-18

  Credit to "OregonTrail" on StackOverflow for ideas on simplifying the logic.
  (https://stackoverflow.com/questions/25028929/24-game-using-python/25029244)
  --------------

  Logic:
    Each round of play consists of four numbers and three operators.
    The four numbers can be arranged in 4!=24 ways (order matters).
    Since, operators can be repeated, there are 4**3=64 operator permutations.
    Therefore we have 24*64=1536 possible permutations of combining 
    the number-seq permuatations with the operator-equence permutations.

    Now, we add to this all the possible permutations of sub-groupings
    of the equation "tokens" with parenthesis and we end up with 6144 equations.

    However, the actual number of mathematically-unique equations is less than this
    due to many of the equations being mathematically equivelent as a result of the
    Commutitive and Associative properties of addition and multiplication:
         * Commutative: 2+3 = 3+2,  and 2*3 = 3*2
         * Associative: (2+4)+3 = 2+(4+3), and (2*3)*4 = 2*(3*4)

    After generating a random sequence of 4 numbers we perform all possible
    mathematical equation permuations (except those involving division-by-zero), 
    iterating over the different number-sequences and operator sequences, and 
    performing all unique parenthesis groupings. Any final calculations that result 
    in 24 are stored.

    TODO: remove all mathematically equivelent solutions.

  --------------
  NOTES:
  1) It is possible (though not ususally done) to arrive at a soltuion by dividing and
     multiplying numbers that are not evenly divisible.
     For example, given the numbers (4, 5, 6, 5):
       a) 4 / 5 = 0.8
       b) 6 * 5 = 30
       c) 30 * 0.8 = 24
"""

import itertools
import random

DEBUG = 0 

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
def find_all_24(ns_list, os_list):
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

  solutions = []
  solution_tokens = []

  tot_equations = 0
  tot_token_permutations = 0

  # Iterate over list of number sequences
  for ns in ns_list: # example (3,3,2,2)

    # Iterate over list of operator-sequences
    for ops in os_list:

        tot_token_permutations += 1 
        dprint(2, "[%d]: %s  %s" % (tot_token_permutations, str(ns), str(ops))) 
        token_set = (ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
        solution_tokens.append( token_set )

        # Now we construct the unique combinations of parenthesis groupings 

        #-------------------
        # 1) Sequential operations: example, for ns=(3,3,2,2): equation=((3+3)*2)*2
        # Don;t have to consider divide-by-zero here since input numbers cannot be 0 
        tot_equations += 1
        result = calc(ns[0], ops[0], ns[1])    # 3+3=6
        result = calc(result, ops[1], ns[2])   # 6*2=12
        result = calc(result, ops[2], ns[3])   # 12*2=24
        if result == 24:
            sol = "((%d%s%d)%s%d)%s%d" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
            dprint(1, ">>> Solution (seq): %s" % (sol) )
            solutions.append( sol )

        #-------------------
        # 2) Paired operations - left/right (p-lr): example, for ns=(8,4,1,1): equation=(8+4)*(1+1)
        tot_equations += 1
        result_l = calc(ns[0], ops[0], ns[1]) # (8+4)=12
        result_r = calc(ns[2], ops[2], ns[3]) # (1+1)=2

        # Pass on any divide-by-zero options
        if ops[1] == '/' and result_r == 0:
            dprint(4, ">>> Ignore div-by-zero (p-lr): (%d/%d) " % (result_l, result_r) )

        else:
          result = calc(result_l, ops[1], result_r) # (12*2)=24
          if result == 24:
              sol = "(%d%s%d)%s(%d%s%d)" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
              dprint(1, ">>> Solution (p-lr): %s" % (sol) )
              solutions.append( sol )

        #-------------------
        # Paired operations - inside/out,*left-right* (p-io-lr): example, for ns=(8,4,3,4): equation=(8 + (4*3))+4 
        tot_equations += 1
        result_m = calc(ns[1], ops[1], ns[2])   # (4*3)=12

        # Pass on any divide-by-zero options
        if ops[0] == '/' and result_m == 0:
            dprint(4, ">>> Ignore div-by-zero (p-io-lr): (%d/%d) " % (ns[0], result_m) )

        else:
          result_ml = calc(ns[0], ops[0], result_m) # (8+12)=20
          result = calc(result_ml, ops[2], ns[3])   # (20+4)=24
          if result == 24:
              sol = "(%d%s(%d%s%d))%s%d" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
              dprint(1, ">>> Solution (p-io-lr): %s" % (sol) )
              solutions.append( sol )

        #-------------------
        # Paired operations - inside/out, *right-left* (p-io-rl): example, for ns=(8,12,6,1): equation=8*((12 / 6) + 1) 
        tot_equations += 1
        result_m = calc(ns[1], ops[1], ns[2])     # (12/6)=2
        result_mr = calc(result_m, ops[2], ns[3]) # (2+1)=3

        # Pass on any divide-by-zero options
        if ops[0] == '/' and result_mr == 0:
            dprint(4, ">>> Ignore div-by-zero (p-io-rl): (%d/%d) " % (ns[0], result_mr) )
        
        else: 
          result = calc(ns[0], ops[0], result_mr) # (8*3)=24
          if result == 24:
              sol = "%d%s((%d%s%d)%s%d)" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
              dprint(1, ">>> Solution (p-io-rl): %s" % (sol) )
              solutions.append( sol )

  dprint(4, "Total-token-permutations: %d" % (tot_token_permutations))
  dprint(2, "Total-equations: %d" % (tot_equations))
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

    solution_list = find_all_24(number_sequences, ops_perms)

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
    games = generate_valid_games(3)
    for game in games:
        solution_list = game['solutions']
        numbers = game['numbers']
        print("NUMBERS: %s" % (numbers))
        print("SOLUTIONS: %d" % len(solution_list))
        for i,s in enumerate(solution_list, start=1):
            print("%d: %s" % (i,str(s)))
        print("\n")
