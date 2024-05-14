class CalcEdit:
    def __init__(self, word_list, alpha):
        self.lexicon = word_list
        self.alphabet = list(alpha)

    def is_cognate_(self, input_word, threshold=1):
        cognates = []
        for word in self.lexicon:
            dl_distance, operations = self.calculate_dl_distance(
                input_word, word, threshold
            )
            if dl_distance <= threshold and dl_distance != -1:
                cognates.append(("score: " + str(dl_distance), word, operations))
        return cognates

    def calculate_dl_distance(self, input_word1, input_word2, dist_limit=1):
        word1 = [""]
        word2 = [""]

        # print(input_word2)

        word1.extend(self.__deconstruct_str(input_word1))
        word2.extend(self.__deconstruct_str(input_word2))

        # if the size difference is more than the limit, it's not worth checking
        if abs(len(word1) - len(word2)) > dist_limit:
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
                # cost is 0 if the letter is the same or 1 if not
                cost = 0 if word1[i - 1] == word2[j - 1] else 1

                insertion = dl_matrix[i][j - 1] + 1
                deletion = dl_matrix[i - 1][j] + 1
                substitution = dl_matrix[i - 1][j - 1] + cost

                min_distance = min(insertion, deletion, substitution)

                if min_distance == insertion:
                    op_matrix[i][j] = "I"
                elif min_distance == deletion:
                    op_matrix[i][j] = "D"
                else:
                    op_matrix[i][j] = "S" if cost == 1 else ""  # substitution

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

        # for row in dl_matrix:
        #     print(row)
        # print("Operations Matrix:")
        # for row in op_matrix:
        #     print(row)

        return dl_matrix[-1][-1], operations

    def __deconstruct_str(self, input_word):
        """
        Deconstructs the string into an array of chars
        """
        word_chars = []

        for char in input_word:
            if char.lower() in self.alphabet:
                word_chars.append(char)

        return word_chars
