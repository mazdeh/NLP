from fst import FST
import string, sys
from fsmutils import composechars, trace

f1 = FST('soundex-generate')

f1.add_state('start')
f1.add_state('next')
f1.initial_state = 'start'
f1.set_final('next')

list_one = ['b', 'f', 'p', 'v']
list_two = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']
list_three = ['d', 't']
list_four = ['l']
list_five = ['m', 'n']
list_six = ['r']
vowels = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y']