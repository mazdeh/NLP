import sys
from fst import FST
from fsmutils import composewords, trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.initial_state = 'start'
    f.add_state('1stzero')
    f.add_state('tens')
    f.add_state('seventeen')
    f.add_state('final_seventeen')
    f.add_state('eighteen')
    f.add_state('final_eighteen')
    f.add_state('nineteen')
    f.add_state('final_nineteen')
    f.add_state('zero')
    f.add_state('ones')
    f.add_state('20-69')
    f.add_state('70-ten')
    f.add_state('80s')
    f.add_state('90s')
    f.add_state('100s')
    f.add_state('et')
    f.add_state('10-et')
    f.add_state('et-un')
    f.add_state('et-onze')

    f.set_final('zero')
    f.set_final('ones')
    f.set_final('tens')
    f.set_final('final_seventeen')
    f.set_final('final_eighteen')
    f.set_final('final_nineteen')
    f.set_final('20-69')
    f.set_final('70-ten')
    f.set_final('80s')
    f.set_final('90s')
    f.set_final('et-un')
    f.set_final('et-onze')


# 100 - 999
    f.add_arc('start', '1stzero', '1', [kFRENCH_TRANS[100]])
    for i in range(2, 10):
        f.add_arc('start', '100s', str(i), [kFRENCH_TRANS[i]])

    f.add_arc('100s', '1stzero', (), [kFRENCH_TRANS[100]])


# 0 - 9
    f.add_arc('start', '1stzero', '0', [])
    f.add_arc('1stzero', 'ones', '0', [])
    for ii in range(1, 10):
        f.add_arc('ones', 'ones', str(ii), [kFRENCH_TRANS[ii]])

    f.add_arc('ones', 'ones', '0', [])
    
    # for i in range(10):
    #     f.add_arc('ten-6', 'ten-6', str(i), kFRENCH_TRANS[(i+10])
# 10 - 16
    f.add_arc('1stzero', 'tens', '1', [])
    f.add_arc('tens', 'tens', '0', [kFRENCH_TRANS[10]])
    f.add_arc('tens', 'tens', '1', [kFRENCH_TRANS[11]])
    f.add_arc('tens', 'tens', '2', [kFRENCH_TRANS[12]])
    f.add_arc('tens', 'tens', '3', [kFRENCH_TRANS[13]])
    f.add_arc('tens', 'tens', '4', [kFRENCH_TRANS[14]])
    f.add_arc('tens', 'tens', '5', [kFRENCH_TRANS[15]])
    f.add_arc('tens', 'tens', '6', [kFRENCH_TRANS[16]])

    f.add_arc('tens', 'seventeen', '7', [kFRENCH_TRANS[10]])
    f.add_arc('seventeen', 'final_seventeen', (), [kFRENCH_TRANS[7]])
    f.add_arc('tens', 'eighteen', '8', [kFRENCH_TRANS[10]])
    f.add_arc('eighteen', 'final_eighteen', (), [kFRENCH_TRANS[8]])
    f.add_arc('tens', 'nineteen', '9', [kFRENCH_TRANS[10]])
    f.add_arc('nineteen', 'final_nineteen', (), [kFRENCH_TRANS[9]])

# 20 - 69
    f.add_arc('1stzero', '20-69', '2', [kFRENCH_TRANS[20]])
    f.add_arc('1stzero', '20-69', '3', [kFRENCH_TRANS[30]])
    f.add_arc('1stzero', '20-69', '4', [kFRENCH_TRANS[40]])
    f.add_arc('1stzero', '20-69', '5', [kFRENCH_TRANS[50]])
    f.add_arc('1stzero', '20-69', '6', [kFRENCH_TRANS[60]])

    # special cases:
    for i in range(2, 10):
        f.add_arc('20-69', '20-69', str(i), [kFRENCH_TRANS[i]])

        # handles 20, 30 ... 60
    for i in range(20, 60, 10):
        f.add_arc('20-69', '20-69', '0', [])

        # handles 21, 31, ... 61
    f.add_arc('20-69', 'et', '1', [kFRENCH_AND])
    f.add_arc('et', 'et-un', (),[kFRENCH_TRANS[1]])

# 70 - 79
    f.add_arc('1stzero', '70-ten', '7', [kFRENCH_TRANS[60]])
    f.add_arc('70-ten', '70-ten', '0', [kFRENCH_TRANS[10]])
    # handle 71 here
    f.add_arc('70-ten', '10-et', '1', [kFRENCH_AND])
    f.add_arc('10-et', 'et-onze', (),[kFRENCH_TRANS[11]])
    f.add_arc('70-ten', '70-ten', '2', [kFRENCH_TRANS[12]])
    f.add_arc('70-ten', '70-ten', '3', [kFRENCH_TRANS[13]])
    f.add_arc('70-ten', '70-ten', '4', [kFRENCH_TRANS[14]])
    f.add_arc('70-ten', '70-ten', '5', [kFRENCH_TRANS[15]])
    f.add_arc('70-ten', '70-ten', '6', [kFRENCH_TRANS[16]])
    
    f.add_arc('70-ten', 'seventeen', '7', [kFRENCH_TRANS[10]])
    f.add_arc('seventeen', 'final_seventeen', (), [kFRENCH_TRANS[7]])
    f.add_arc('70-ten', 'eighteen', '8', [kFRENCH_TRANS[10]])
    f.add_arc('eighteen', 'final_eighteen', (), [kFRENCH_TRANS[8]])
    f.add_arc('70-ten', 'nineteen', '9', [kFRENCH_TRANS[10]])
    f.add_arc('nineteen', 'final_nineteen', (), [kFRENCH_TRANS[9]])

# 80 - 89
    f.add_arc('1stzero', '80s', '8', [kFRENCH_TRANS[4]])
    f.add_arc('80s', 'ones', (), [kFRENCH_TRANS[20]])
    f.add_arc('80s', '80s', '0', [kFRENCH_TRANS[20]])

# 90 - 99
    f.add_arc('1stzero', '90s', '9', [kFRENCH_TRANS[4]])
    f.add_arc('90s', 'tens', (), [kFRENCH_TRANS[20]])

    return f


if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))

