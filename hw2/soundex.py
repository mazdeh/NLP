from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('next')
    f1.add_state('one')
    f1.add_state('two')
    f1.add_state('three')
    f1.add_state('four')
    f1.add_state('five')
    f1.add_state('six')
    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('next')
    f1.set_final('one')
    f1.set_final('two')
    f1.set_final('three')
    f1.set_final('four')
    f1.set_final('five')
    f1.set_final('six')

    list_one = ['b', 'f', 'p', 'v']
    list_two = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']
    list_three = ['d', 't']
    list_four = ['l']
    list_five = ['m', 'n']
    list_six = ['r']
    vowels = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y']

    # Add the rest of the arcs
     # changed string.ascii_lowercase to string.letters
    
    for letter in string.letters:
        f1.add_arc('start', 'next', (letter), (letter))

    for letter in string.letters:
        if letter in list_one:
            f1.add_arc('next', 'one', (letter), '1')
        elif letter in list_two:
            f1.add_arc('next', 'two', (letter), '2')
        elif letter in list_three:
            f1.add_arc('next', 'three', (letter), '3')
        elif letter in list_four:
            f1.add_arc('next', 'four', (letter), '4')
        elif letter in list_five:
            f1.add_arc('next', 'five', (letter), '5')
        elif letter in list_six:
            f1.add_arc('next', 'six', (letter), '6')
        else:
            f1.add_arc('next', 'next', (letter), ())

    for letter in string.letters:
        if letter in list_two:
            f1.add_arc('one', 'two', (letter), '2')
        elif letter in list_three:
            f1.add_arc('one', 'three', (letter), '3')
        elif letter in list_four:
            f1.add_arc('one', 'four', (letter), '4')
        elif letter in list_five:
            f1.add_arc('one', 'five', (letter), '5')
        elif letter in list_six:
            f1.add_arc('one', 'six', (letter), '6')
        else:
            f1.add_arc('one', 'one', (letter), ())

    for letter in string.letters:
        if letter in list_one:
            f1.add_arc('two', 'one', (letter), '1')
        elif letter in list_three:
            f1.add_arc('two', 'three', (letter), '3')
        elif letter in list_four:
            f1.add_arc('two', 'four', (letter), '4')
        elif letter in list_five:
            f1.add_arc('two', 'five', (letter), '5')
        elif letter in list_six:
            f1.add_arc('two', 'six', (letter), '6')
        else:
            f1.add_arc('two', 'two', (letter), ())

    for letter in string.letters:
        if letter in list_one:
            f1.add_arc('three', 'one', (letter), '1')
        elif letter in list_two:
            f1.add_arc('three', 'two', (letter), '2')
        elif letter in list_four:
            f1.add_arc('three', 'four', (letter), '4')
        elif letter in list_five:
            f1.add_arc('three', 'five', (letter), '5')
        elif letter in list_six:
            f1.add_arc('three', 'six', (letter), '6')
        else:
            f1.add_arc('three', 'three', (letter), ())

    for letter in string.letters:
        if letter in list_one:
            f1.add_arc('four', 'one', (letter), '1')
        elif letter in list_two:
            f1.add_arc('four', 'two', (letter), '2')
        elif letter in list_three:
            f1.add_arc('four', 'three', (letter), '3')
        elif letter in list_five:
            f1.add_arc('four', 'five', (letter), '5')
        elif letter in list_six:
            f1.add_arc('four', 'six', (letter), '6')
        else:
            f1.add_arc('four', 'four', (letter), ())

    for letter in string.letters:
        if letter in list_one:
            f1.add_arc('five', 'one', (letter), '1')
        elif letter in list_two:
            f1.add_arc('five', 'two', (letter), '2')
        elif letter in list_three:
            f1.add_arc('five', 'three', (letter), '3')
        elif letter in list_four:
            f1.add_arc('five', 'four', (letter), '4')
        elif letter in list_six:
            f1.add_arc('five', 'six', (letter), '6')
        else:
            f1.add_arc('five', 'five', (letter), ())

    for letter in string.letters:
        if letter in list_one:
            f1.add_arc('six', 'one', (letter), '1')
        elif letter in list_two:
            f1.add_arc('six', 'two', (letter), '2')
        elif letter in list_three:
            f1.add_arc('six', 'three', (letter), '3')
        elif letter in list_four:
            f1.add_arc('six', 'four', (letter), '4')
        elif letter in list_five:
            f1.add_arc('six', 'five', (letter), '5')
        else:
            f1.add_arc('six', 'six', (letter), ())
    return f1

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.add_state('5')
    f2.initial_state = '1'
    f2.set_final('5')
    f2.set_final('4')
    f2.set_final('3')
    f2.set_final('2')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('1', '1', (letter), (letter))

    for n in range(1,10):
        f2.add_arc('1', '2', str(n), str(n))

    for n in range(1,10):
        f2.add_arc('2', '3', str(n), str(n))

    for n in range(1,10):
        f2.add_arc('3', '4', str(n), str(n))

    for n in range(1,10):
        f2.add_arc('4', '4', str(n), ())
    return f2

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')
    f3.add_state('5')
    
    f3.initial_state = '1'
    f3.set_final('4')
    f3.set_final('1')

    f3.add_arc('1', '4', (), '000')
    f3.add_arc('2', '4', (), '00')
    f3.add_arc('3', '4', (), '0')

    for letter in string.letters:
        f3.add_arc('1', '1', letter, letter)
    for number in range(10):
        f3.add_arc('1', '2', str(number), str(number))
    for number in range(10):
        f3.add_arc('2', '3', str(number), str(number))
    for number in range(10):
        f3.add_arc('3', '4', str(number), str(number))
    for number in range(10):
        f3.add_arc('4', '4', str(number), ())
    return f3

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
