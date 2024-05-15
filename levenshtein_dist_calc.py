class LevenshteinDistanceCalculator:
    def __init__(self, word_list, alpha):
        """
        Args:
            word_list (list): A list of words used for finding cognates.
            alpha (str): A string representing the alphabet used in the word list.
        """
        self.lexicon = word_list
        self.alphabet = list(alpha)  # convert alpha string to list
        # placeholder: substitution table for directed distance between phonenmes

    def is_cognate_(self, input_word, threshold=1):
        """
        Determines possible cognates within the lexicon for a given word based on the Damerau-Levenshtein distance.

        Args:
            input_word (str): The word to compare against the lexicon.
            threshold (int): The maximum allowed distance to consider a word a cognate.

        Returns:
            list: A list of tuples with the distance score, the cognate word, and the operations needed to convert input_word to the cognate.
        """
        cognates = []
        for word in self.lexicon:
            dl_distance, operations = self.calculate_dl_distance(
                input_word, word, threshold
            )
            if dl_distance <= threshold and dl_distance != -1:
                cognates.append(("score: " + str(dl_distance), word, operations))
        return cognates

    def get_distance_matrix(self, cognates: list) -> list:
        """
        Generates a 2d distance matrix between all proposed cognates for a given concept regularized by
        the length of the longer string in each comparison. These are stored in cells of an n by n matrix.
        Missing entries in cognate pairs are stored as nan values.

        Args:
            cognates (list): list of proposed cognates to be compared with eachother.

        Returns:
            list: n x n distance list
        """
        distance_matrix = [
            [0 for i in range(len(cognates))] for j in range(len(cognates))
        ]

        for i, source in enumerate(cognates):
            for j, target in enumerate(cognates):
                if (
                    source == "" or target == ""
                ):  # if one cognate in pair is missing, null value
                    distance_matrix[i][j] = float("nan")
                else:
                    distance_matrix[i][j] = self.calculate_dl_distance(
                        source, target, 1000
                    )[0] / max(len(source), len(target))

        return distance_matrix

    def get_all_dl_distances(self, data_df, threshold=100):
        """
        Computes the Damerau-Levenshtein distance for all pairs in a dataset.

        Args:
            data_df (DataFrame): A DataFrame where each row contains different language versions of the same word.
            threshold (int): Distance threshold to filter out unlikely cognates.

        Returns:
            list: A list containing dictionaries for each row in the DataFrame with the word, cognates, and their scores.
        """
        all_word_scores = []
        language_names = data_df.iloc[0].values.tolist()

        for index, row in data_df.iterrows():
            row_dict = {}

            index_word = data_df.iloc[index, 0]
            index_word = index_word.split()
            index_word = " ".join(index_word[1:])
            row_dict["EnglishWord"] = index_word

            row_dict["cognates"] = []

            tokens = [
                (data_df.columns[i + 1], token)
                for i, token in enumerate(row[1:])
                if token != ""
            ]

            for i, (lang1_id, word1) in enumerate(tokens):
                for j, (lang2_id, word2) in enumerate(tokens[i + 1 :]):

                    dl_distance, operations = self.calculate_dl_distance(
                        word1, word2, threshold=threshold
                    )
                    if 0 < dl_distance <= threshold:
                        row_dict["cognates"].append(
                            {
                                "word1": word1,
                                "lang1": language_names[lang1_id],
                                "word2": word2,
                                "lang2": language_names[lang2_id],
                                "score": dl_distance,
                                # "operations": operations,
                            }
                        )
            all_word_scores.append(row_dict)

        return all_word_scores

    def calculate_dl_distance(self, input_word1, input_word2, threshold=1):
        """
        Calculates the Damerau-Levenshtein distance using the Wagner-Fischer algorithm.

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
