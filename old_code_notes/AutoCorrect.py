"""
Class that is an instance of AutoCorrect that uses a lexicon and
an alphabet to compare words against. It 
"""


class AutoCorrect:
    def __init__(self, word_list, alpha):
        self.LEXICON = word_list
        self.ALPHABET = [*alpha]

    # Used dynamic programming method, so skipped these 3 methods
    def insertion(self, input_word):
        pass

    def deletion(self, input_word):
        pass

    def substitution(self, input_word):
        pass

    # Function that checks if the incorrect word is simply a character swap mistake
    def swapping(self, input_word):
        word_chars = self.__deconstruct_str(input_word)
        fixed_word = None

        for i in range(1, len(word_chars)):
            temp_word = word_chars[:]
            temp_word[i - 1], temp_word[i] = temp_word[i], temp_word[i - 1]
            new_word = "".join(temp_word)

            # mixed up new word is found in the lexicon
            if new_word in self.LEXICON:
                fixed_word = new_word

        return fixed_word

    # Function that perform an edit on a word that is not in a lexicon
    def edit(self, input_word):
        choices = []

        # try swapping first
        try_swap = self.swapping(input_word)
        if try_swap != None:
            choices.append(try_swap)
            return choices, "swapped"

        # look through every word in the lexicon and see what words are close to it
        for word in self.LEXICON:
            if self.__calculate_dl_distance(input_word, word) == 1:
                choices.append(word)

        # catch all if nothing is found
        if choices == None:
            return "", ""

        return choices, ""

    # Function that takes in a 2 words and calculates the Damerau–Levenshtein distance of them
    def __calculate_dl_distance(self, input_word1, input_word2, dist_limit=1):
        word1 = [""]
        word2 = [""]

        word1.extend(self.__deconstruct_str(input_word1))
        word2.extend(self.__deconstruct_str(input_word2))

        # if the size difference is more than the limit, it's not worth checking
        if abs(len(word1) - len(word2)) > dist_limit:
            return None

        dl_matrix = []
        for i in range(len(word2)):
            dl_matrix.append([])
            for j in range(len(word1)):
                # cost is 0 if the letter is the same or 1 if not
                cost = 0 if word1[j] == word2[i] else 1

                # initial position in a row
                if j == 0:
                    dl_matrix[i].append(i)
                # initialize first row
                elif len(dl_matrix) == 1:
                    dl_matrix[i].append(j)
                else:
                    insertion = dl_matrix[i][j - 1] + 1
                    deletion = dl_matrix[i - 1][j] + 1
                    substitution = dl_matrix[i - 1][j - 1] + cost

                    dl_matrix[i].append(min(insertion, deletion, substitution))

        return dl_matrix[-1][-1]

    # Deconstructs the string into an array of chars
    def __deconstruct_str(self, input_word):
        word_chars = []

        for char in input_word:
            if char.upper() in self.ALPHABET:
                word_chars.append(char)

        return word_chars
#comment