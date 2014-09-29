from math import log, exp
from collections import defaultdict
from string import lower
import argparse

from numpy import mean

import nltk
from nltk import FreqDist
from nltk.util import bigrams
from nltk.tokenize import TreebankWordTokenizer

kLM_ORDER = 2
kUNK_CUTOFF = 3
kNEG_INF = -1e6

kSTART = "<s>"
kEND = "</s>"

def lg(x):
    return log(x) / log(2.0)

class BigramLanguageModel:

    def __init__(self, unk_cutoff, jm_lambda=0.6, dirichlet_alpha=0.1,
                 katz_cutoff=5, kn_discount=0.1, kn_concentration=1.0,
                 tokenize_function=TreebankWordTokenizer().tokenize,
                 normalize_function=lower):
        self._unk_cutoff = unk_cutoff
        self._jm_lambda = jm_lambda
        self._dirichlet_alpha = dirichlet_alpha
        self._katz_cutoff = katz_cutoff
        self._kn_concentration = kn_concentration
        self._kn_discount = kn_discount
        self._vocab_final = False

        self._tokenizer = tokenize_function
        self._normalizer = normalize_function
        
        # Add your code here!

    def train_seen(self, word, count=1):
        """
        Tells the language model that a word has been seen @count times.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final, \
            "Trying to add new words to finalized vocab"

        # Add your code here!
        brown_tokens = nltk.corpus.brown.words()
        counts = brown_tokens.count(word)
        yield counts

    def tokenize(self, sent):
        """
        Returns a generator over tokens in the sentence.  

        You don't need to modify this code.
        """
        for ii in self._tokenizer(sent):
            yield ii
        
    def vocab_lookup(self, word):
        """
        Given a word, provides a vocabulary representation.  Words under the
        cutoff threshold shold have the same value.  All words with counts
        greater than or equal to the cutoff should be unique and consistent.
        """
        assert self._vocab_final, \
            "Vocab must be finalized before looking up words"
        if self.train_seen(word) >= kUNK_CUTOFF:
            return word
        else:
            return -1

    def finalize(self):
        """
        Fixes the vocabulary as static, prevents keeping additional vocab from
        being added
        """
        self._vocab_final = True

    def tokenize_and_censor(self, sentence):
        """
        Given a sentence, yields a sentence suitable for training or
        testing.  Prefix the sentence with <s>, replace words not in
        the vocabulary with <UNK>, and end the sentence with </s>.
        """
        yield self.vocab_lookup(kSTART)
        for ii in self._tokenizer(sentence):
            yield self.vocab_lookup(self._normalizer(ii))
        yield self.vocab_lookup(kEND)


    def normalize(self, word):
        """
        Normalize a word
        """
        return self._normalizer(word)


    def mle(self, context, word):
        """
        Return the log MLE estimate of a word given a context.  If the
        MLE would be negative infinity, use kNEG_INF
        """

        return 0.0

    def laplace(self, context, word):
        """
        Return the log MLE estimate of a word given a context.
        """

        return 0.0

    def good_turing(self, context, word):
        """
        Return the Good Turing probability of a word given a context
        """
        return 0.0

    def jelinek_mercer(self, context, word):
        """
        Return the Jelinek-Mercer log probability estimate of a word
        given a context; interpolates context probability with the
        overall corpus probability.
        """
        return 0.0

    def kneser_ney(self, context, word):
        """
        Return the log probability of a word given a context given
        Kneser Ney backoff
        """
        return 0.0

    def dirichlet(self, context, word):
        """
        Additive smoothing, assuming independent Dirichlets with fixed
        hyperparameter.
        """
        return 0.0

    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # You'll need to complete this function, but here's a line of code that
        # will hopefully get you started.
        for context, word in bigrams(self.tokenize_and_censor(sentence)):
            None

    def perplexity(self, sentence, method):
        """
        Compute the perplexity of a sentence given a estimation method
        """
        return 2.0 ** (-1.0 * mean([method(context, word) for context, word in \
                                    bigrams(self.tokenize_and_censor(sentence))]))

    def sample(self, samples=25):
        """
        Sample words from the language model.
        
        @arg samples The number of samples to return.
        """
        yield ""
        return
