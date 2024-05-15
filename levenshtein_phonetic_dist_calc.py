import panphon.distance


class LevenshteinPhoneticDistanceCalculator:
    def __init__(self, alpha):
        """
        Args:
            alpha (str): A string representing the alphabet used in the word list.
        """
        self.alphabet = list(alpha)
        self.distance = panphon.distance.Distance()

    def calculate_dl_distance(self, input_word1, input_word2, threshold=1):
        """
        Calculates the Damerau-Levenshtein distance using the Wagner-Fischer algorithm and
        uses the Panphon package to calculate the phonetic distance to use as the cost.

        Args:
            input_word1 (str): First word for comparison.
            input_word2 (str): Second word for comparison.
            threshold (int): Maximum size difference between words to consider for distance calculation.

        Returns:
            tuple: A tuple containing:
                the minimum edit distance
                a list of operations used to transform input_word1 to input_word2
        """
        word1 = [""]
        word2 = [""]

        word1.extend(self.__deconstruct_str(input_word1))
        word2.extend(self.__deconstruct_str(input_word2))

        # if the size difference is more than the limit, it's not worth checking
        if abs(len(word1) - len(word2)) > threshold:
            return -1, []

        # init dl matrix and operation matrix
        dl_matrix = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]
        op_matrix = [[""] * (len(word2) + 1) for _ in range(len(word1) + 1)]

        # init first row
        for i in range(len(word1) + 1):
            dl_matrix[i][0] = i
            op_matrix[i][0] = "D"  # deletion

        # init first column
        for j in range(len(word2) + 1):
            dl_matrix[0][j] = j
            op_matrix[0][j] = "I"  # insertion

        for i in range(1, len(word1) + 1):
            for j in range(1, len(word2) + 1):
                # calculate the cost dependent on the phonetic difference
                if word1[i - 1] == word2[j - 1]:
                    cost = 0
                else:
                    cost = self.distance.weighted_feature_edit_distance(
                        word1[i - 1], word2[j - 1]
                    )

                insertion = dl_matrix[i][j - 1] + 1
                deletion = dl_matrix[i - 1][j] + 1
                substitution = dl_matrix[i - 1][j - 1] + cost

                min_distance = min(insertion, deletion, substitution)

                if min_distance == insertion:
                    op_matrix[i][j] = "I"
                elif min_distance == deletion:
                    op_matrix[i][j] = "D"
                else:
                    if cost == 0:
                        op_matrix[i][j] = ""
                    else:
                        op_matrix[i][j] = "S"

                dl_matrix[i][j] = min_distance

        # backtrack
        i, j = len(word1), len(word2)
        operations = []

        while i > 0 or j > 0:
            if i > 0 and j > 0 and op_matrix[i][j] == "S":
                operations.append(f"Substitute '{word1[i - 1]}' with '{word2[j - 1]}'")
                i -= 1
                j -= 1
            elif i > 0 and op_matrix[i][j] == "D":
                operations.append(f"Delete '{word1[i - 1]}'")
                i -= 1
            elif j > 0 and op_matrix[i][j] == "I":
                operations.append(f"Insert '{word2[j - 1]}'")
                j -= 1
            else:
                operations.append(f"Keep '{word2[j - 1]}'")
                i -= 1
                j -= 1

        operations.reverse()
        # remove extra thing
        operations = operations[1:]

        return dl_matrix[-1][-1], operations

    def __deconstruct_str(self, input_word):
        """
        Deconstructs the string into an array of chars.

        Args:
            input_word (str): Word to be deconstructed

        Returns:
            list: The list of characters of the input word
        """
        word_chars = []

        for char in input_word:
            if char.lower() in self.alphabet:
                word_chars.append(char)

        return word_chars
