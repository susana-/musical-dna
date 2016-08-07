'''
Getting the DNA combinations for letters 'ACGT'.

Author(s):
	Ana Parra Vera

References:
	itertools module - https://docs.python.org/2/library/itertools.html
	Learn Python the Hard Way - Exercises 18 and 20

'''

import itertools

def dna_combos():
    """Takes in n letters and returns the possible 2-letter combinations of them"""
    
    prod = itertools.product('ACGT', repeat=2)
    #product will be in the form: {('A, A'), ('A, C'), ('A, G') ...}

    combos = ""

    for i in prod:
    	#copies product in string combos and strips parentheses, quotations and comma
    	combos+=str(i).strip('(\')')+"\n"		#strips outter quotations and parentheses
    	combos = combos.replace("\', \'", "")	#strips inner quotations and comma

    combos = combos.rstrip()    				#removes last \n from string combos
    return combos

print dna_combos()
