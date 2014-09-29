# Author: Vahid Mazdeh
# Date: 09/11/2014

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import *
from nltk.tokenize import word_tokenize
import re


class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        pron = nltk.corpus.cmudict.dict()
        
        try:
            num = pron[word]

        except KeyError:
            return 1
        
        """ takes the shortest pron which is the same as the first pron """
        num = num[0]

        mylist = []
        for i in num:
            if i[-1].isdigit():
                mylist += [i]
        return len(mylist)

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        pron = nltk.corpus.cmudict.dict()

        try:
            a_pron_multiple = pron[a]
            b_pron_multiple = pron[b]

        except KeyError:
            return False
        themin = min(len(a_pron_multiple), len(b_pron_multiple))
        themax = max(len(a_pron_multiple), len(b_pron_multiple))
        m = 0
        for i in range(len(a_pron_multiple)):
                for j in range(len(b_pron_multiple)):
                    a_pron = a_pron_multiple[i]
                    b_pron = b_pron_multiple[j]
                    iterator = min(len(a_pron), len(b_pron))
                    for k in range(1, iterator):
                        if a_pron[-k] != b_pron[-k]:
                            m = 0
                            break
                        else:
                            m = 1
                    if m == 1:
                        return True
        return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).
        
        """
        regex = re.compile(r'\b(\w+)((,|.)|(\s*))(\s*)(\n|$)')
        regex_list = regex.findall(text)
        if len(regex_list) != 5:
            return False
        last_words_list = []
        for i in range(5):
            last_words_list.append(regex_list[i][0])

        if self.rhymes(last_words_list[0], last_words_list[1]):
            if self.rhymes(last_words_list[2], last_words_list[3]):
                if self.rhymes(last_words_list[0], last_words_list[4]):
                    return True

        return False

if __name__ == "__main__":
    buffer = ""
    inline = " "
    while inline != "":
        buffer += "%s\n" % inline
        inline = raw_input()

    ld = LimerickDetector()
    print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))
