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
    Each round of play consists of four numbers and three operators. A random
    sequence of four numbers is generated on each round. The four numbers can
    be arranged in 4!=24 ways (order matters).  Since, operators can be repeated,
    there are 4**3=64 operator permutations.  Therefore we have 24*64=1536 possible
    permutations of combining the number-seq permuatations with the operator-equence
    permutations.
    Now, we add to this all the possible permutations of sub-groupings of
    equation "tokens" by parenthesis which results in 5568 total possible equations.
    If a number is repeated in the number-sequence there will be duplicate equations
    which we skip. Of the remaining equations, the actual number of equations that
    are *mathematically-unique* is less than this due to many of the equations
    being mathematically equivelent as a result of the Commutitive and Associative
    properties of addition and multiplication:
         * Commutative: 2+3 = 3+2,  and 2*3 = 3*2
         * Associative: (2+4)+3 = 2+(4+3), and (2*3)*4 = 2*(3*4)
    Currently, we are not skipping *mathematically equivelent* equations.

    For each new equation, we start calculating the result, checking for and skipping
    any equation that inovlves division-by-zero.  Any final calculations that result
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

# Generate al permuations of 3 operator sequences (with repeat), calculated by the Cartesion-product
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
def check_sequential(num_list, op_list):
    """
     Simple (sequential) arithmetic check for result=24 when there is either no 
     grouping required, such as 1+7+8+8, or when grouping is sequential from 
     left-to-right - i.e. ((3+3)*2)*2
     Args:
      * num_list: list of 4 numbers
      * op_list: list of 3 operators
     Return: valid True|False (whether calculation results in a valid "24" solution) 
    """
                        
    dprint(4, " *check_sequential(%s, %s)" % (num_list, op_list) )
   
    valid = False             
    result = calc(num_list[0], op_list[0], num_list[1]) # 3+3=6
    result = calc(result, op_list[1], num_list[2])      # 6*2=12
    result = calc(result, op_list[2], num_list[3])      # 12*2=24
    if result == 24:
        valid = True
    
    return valid 

#-----------------------------------------------------------------------------------------
def check_paired(num_list, op_list):
    """
     Arithmetic check for result=24 when grouping the equation with simple left and right
     number pairs - i.e. (8+4)*(1+2)
     Args:
      * num_list: list of 4 numbers
      * op_list: list of 3 operators
     Return: valid True|False (whether calculation results in a valid "24" solution) 
    """
                        
    dprint(4, " *check_paired_lr(%s, %s)" % (num_list, op_list) )
                    
    valid = False             
    result_l = calc(num_list[0], op_list[0], num_list[1]) # (8+4)=12
    result_r = calc(num_list[2], op_list[2], num_list[3]) # (1+1)=2
  
    # Pass on any divide-by-zero options
    if op_list[1] == '/' and result_r == 0:
        dprint(3, ">>> Ignore div-by-zero (p-lr): (%d/%d) " % (result_l, result_r) )
  
    else:
        result = calc(result_l, op_list[1], result_r) # (12*2)=24
        if result == 24:
            valid = True

    return valid 

#-----------------------------------------------------------------------------------------
def check_grouped_middle_left(num_list, op_list):
    """
     Arithmetic check for result=24 when grouping the equation from inner-most pair to 
     left side - i.e.  for num_list=(8,4,3,4) equation=(8+(4*3))+4
     Args:
      * num_list: list of 4 numbers
      * op_list: list of 3 operators
     Return: valid True|False (whether calculation results in a valid "24" solution) 
    """
                        
    dprint(4, " *check_grouped_middle_left(%s, %s)" % (num_list, op_list) )
                    
    valid = False
    # middle grouping 
    result_m = calc(num_list[1], op_list[1], num_list[2])   # (4*3)=12

    # Pass on any divide-by-zero options
    if op_list[0] == '/' and result_m == 0:
        dprint(3, ">>> Ignore div-by-zero (g-ml): (%d/%d) " % (num_list[0], result_m) )

    else:
        result_ml = calc(num_list[0], op_list[0], result_m) # (8+12)=20
        result = calc(result_ml, op_list[2], num_list[3])   # (20+4)=24
        if result == 24:
            valid = True

    return valid 

#-----------------------------------------------------------------------------------------
def check_grouped_middle_right(num_list, op_list):
    """
     Arithmetic check for result=24 when grouping the equation from inner-most pair to 
     right side - i.e.  for num_list=(8,12,6,1) equation=8*((12 / 6) + 1)
     Args:
      * num_list: list of 4 numbers
      * op_list: list of 3 operators
     Return: valid True|False (whether calculation results in a valid "24" solution) 
    """
                        
    dprint(4, " *check_grouped_middle_right(%s, %s)" % (num_list, op_list) )
                    
    valid = False
    # middle grouping 
    result_m = calc(num_list[1], op_list[1], num_list[2])   # (12/6)=2
    result_mr = calc(result_m, op_list[2], num_list[3])     # (2+1)=3

    # Pass on any divide-by-zero options
    if op_list[0] == '/' and result_mr == 0:
        dprint(3, ">>> Ignore div-by-zero (g-mr): (%d/%d) " % (num_list[0], result_mr) )

    else:
        result = calc(num_list[0], op_list[0], result_mr) # (8*3)=24
        if result == 24:
            valid = True

    return valid 

#-----------------------------------------------------------------------------------------
def find_all_24(ns_list, os_list):
    """
     Take a list of 4-digit tuples, and a list of 3-operator tuples, for example ('+' '*', '*')
     and determine if 24 can be made from any of the combined mathematical operations.
     Store all valid solutions.
     Args:
      * ns_list: list of number-sequence tuples, each containing uniq permutation of 4 numbers
      * os_list: list of operator-sequence tuples, each containing uniq permutation of 3 operators
     Return: list of valid solutions. Can be empty!
    """

    solutions = []

    # Since numbers and operators can be repeated, we can end up with duplicate equations across
    # the various permutations.  We will skip any duplicate equations.

    tot_equations = 0

    # Iterate over list of number sequences
    for ns in ns_list: # example (3,3,2,2)

        # Iterate over list of operator-sequences
        for ops in os_list:
    

            # If we ONLY have + and -, we don't need any groupings
            if '*' not in ops and '/' not in ops:
                equation = "%d%s%d%s%d%s%d" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
                if equation in solutions:
                    dprint(1, ">>> Skipping duplicate solution (simple): %s" % (equation) )
                else:
                    tot_equations += 1
                    if check_sequential(ns, ops): 
                        dprint(1, ">>> Solution (simple): %s" % (equation) )
                        solutions.append( equation )

            # Otherwise, we need to check all the unique combinations of parenthesis groupings
            else:

                #-------------------
                # 1) Sequential operations: example, for ns=(3,3,2,2): equation=((3+3)*2)*2
                # Don't have to consider divide-by-zero here since input numbers cannot be 0
  
                equation = "((%d%s%d)%s%d)%s%d" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
                if equation in solutions:
                    dprint(1, ">>> Skipping duplicate solution (seq): %s" % (equation) )
                else:
                    tot_equations += 1
                    if check_sequential(ns, ops): 
                        dprint(1, ">>> Solution (seq): %s" % (equation) )
                        solutions.append( equation )

                #-------------------
                # 2) Paired operations - left/right (p-lr): example, for ns=(8,4,1,1): equation=(8+4)*(1+1)
  
                equation = "(%d%s%d)%s(%d%s%d)" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
                if equation in solutions:
                    dprint(1, ">>> Skipping duplicate solution (p-lr): %s" % (equation) )
                else:
                    tot_equations += 1
                    if check_paired(ns, ops): 
                        dprint(1, ">>> Solution (p-lr): %s" % (equation) )
                        solutions.append( equation )

                #-------------------
                # 3) Grouped operations - middle,left* (g-ml): example, for ns=(8,4,3,4): equation=(8 + (4*3))+4
  
                equation = "(%d%s(%d%s%d))%s%d" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
                if equation in solutions:
                    dprint(1, ">>> Skipping duplicate solution (g-ml): %s" % (equation) )
                else:
                    tot_equations += 1
                    if check_grouped_middle_left(ns, ops): 
                        dprint(1, ">>> Solution (g-ml): %s" % (equation) )
                        solutions.append( equation )


                #-------------------
                # 4) Grouped operations - middle,right (g-mr): example, for ns=(8,12,6,1): equation=8*((12 / 6) + 1)
  
                equation = "%d%s((%d%s%d)%s%d)" % ( ns[0], ops[0], ns[1], ops[1], ns[2], ops[2], ns[3] )
                if equation in solutions:
                    dprint(1, ">>> Skipping duplicate solution (g-mr): %s" % (equation) )
                else:
                    tot_equations += 1
                    if check_grouped_middle_right(ns, ops): 
                        dprint(1, ">>> Solution (g-mr): %s" % (equation) )
                        solutions.append( equation )

    dprint(2, "Total-equations checked: %d" % (tot_equations))

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
def build_game(number_list=None):
    """
     Create a game "result object" (4 numbers and all solutions).
     If number_list is None, create the 4 input numbers at random.
     If number_list is populated , create the solutions with those numbers.
     Return: result object { 'numbers': [x,x,x,x], 'solutions': [] }
    """
    n4 = number_list
    if number_list is None:
        n4 = get_random_four()

    number_sequences = get_num_permutations(n4)

    dprint(4, "NS: %s" % number_sequences)
    dprint(4, "OPS (%d): %s" % (len(ops_perms), ops_perms), end="\n\n")

    solution_list = find_all_24(number_sequences, ops_perms)

    result = {
     'numbers': n4,
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
    while len(games) < N:
        game = build_game()
        N_solutions = len(game['solutions'])
        if N_solutions:
            games.append(game)

    return games

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':

    ## Perfom a single game from input numbers
    n4 = [2,4,5,7]
#    n4 = [1,7,8,8]
    game = build_game(n4)
    numbers = game['numbers']
    solution_list = game['solutions']
    print("NUMBERS: %s" % (numbers))
    print("SOLUTIONS: %d" % len(solution_list))
    for i,s in enumerate(solution_list, start=1):
        print("%d: %s" % (i,str(s)))
    print("\n------------------------\n")

    ## Perfom a single game from random numbers
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
    for n,game in enumerate(games, start=1):
        solution_list = game['solutions']
        numbers = game['numbers']
        print("Game-%d NUMBERS: %s" % (n,numbers))
        print("Game-%d SOLUTIONS: %d" % (n,len(solution_list)))
        for i,s in enumerate(solution_list, start=1):
            print("%d: %s" % (i,str(s)))
        print("\n")
