import panphon.distance


class LevenshteinDistanceCalculator:
    def __init__(self, use_phonetic=False):  # df, alpha, use_phonetic=False):
        """
        Args:
            df (pandas dataframe): The forms data of a language family containing cognates as strings
            alpha (str): A string representing the alphabet used in the word list.
            use_phonetic (bool): Uses a phonetic distance instead of 1 for the cost during calculation if true
        """
        # self.df = df
        # self.alphabet = list(alpha)  # convert alpha string to list
        self.use_phonetic = use_phonetic

        # placeholder: substitution table for directed distance between phonenmes

        self.distance = panphon.distance.Distance()

    def get_distance_matrices(self):
        """
        Generates a list of 2d distance matrices between all proposed cognates for each concept in a given data frame
        regularized by the length of the longer string in each comparison. These are stored in cells of an n by n matrix.
        Missing entries in cognate pairs are stored as nan values.

        Args:
            df: pandas data frame with form data for some language family

        Returns:
            list: a list of n x n distance lists for each concept in order
        """
        distances = []
        for row in range(len(self.df)):
            if row != 0:
                cognates = self.df.loc[row][1:]  # The cognates of 1 row (1 concept)
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
                distances.append(distance_matrix)
        return distances

    def get_all_dl_distances(self, threshold=100):
        """
        Computes the Damerau-Levenshtein distance for all pairs in a dataset.

        Args:
            data_df (DataFrame): A DataFrame where each row contains different language versions of the same word.
            threshold (int): Distance threshold to filter out unlikely cognates.

        Returns:
            list: A list containing dictionaries for each row in the DataFrame with the word, cognates, and their scores.
                Ex: [{'lexeme': 'the land',
                    'cognates': [{'word1': 'su', 'lang1': 'Awa Pit', 'word2': 'to', 'lang2': 'Tsafiki', 'score': 1.0},
                                {'word1': 'tu', 'lang1': "Cha'palaa", 'word2': 'to', 'lang2': 'Tsafiki', 'score': 1.0}]}]
        """
        all_word_scores = []
        language_names = self.df.iloc[0].values.tolist()

        for index, row in self.df.iterrows():
            row_dict = {}

            index_word = self.df.iloc[index, 0]
            index_word = index_word.split()
            index_word = " ".join(index_word[1:])
            row_dict["lexeme"] = index_word
            row_dict["cognates"] = []

            # list of tuples (lang index, token)
            tokens = [
                (self.df.columns[i + 1], token)
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

    def calculate_dl_distance(self, input_word1, input_word2, threshold=4):
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
        dl_matrix = [[0] * (len(word2)) for _ in range(len(word1))]
        op_matrix = [[""] * (len(word2)) for _ in range(len(word1))]

        # init first row
        for i in range(len(word1)):
            dl_matrix[i][0] = i
            op_matrix[i][0] = "D"  # deletion

        # init first column
        for j in range(len(word2)):
            dl_matrix[0][j] = j
            op_matrix[0][j] = "I"  # insertion

        for i in range(1, len(word1)):
            for j in range(1, len(word2)):
                # cost is 0 if the letter is the same or 1 if not
                if word1[i] == word2[j]:
                    cost = 0
                else:
                    if self.use_phonetic:
                        cost = self.distance.weighted_feature_edit_distance(
                            word1[i], word2[j]
                        )
                    else:
                        cost = 1

                insertion_cost = dl_matrix[i][j - 1] + 1
                deletion_cost = dl_matrix[i - 1][j] + 1
                substitution_cost = dl_matrix[i - 1][j - 1] + cost

                min_distance = min(insertion_cost, deletion_cost, substitution_cost)
                dl_matrix[i][j] = min_distance

                if min_distance == insertion_cost:
                    op_matrix[i][j] = "I"
                elif min_distance == deletion_cost:
                    op_matrix[i][j] = "D"
                else:
                    if cost == 0:
                        op_matrix[i][j] = ""  # keep
                    else:
                        op_matrix[i][j] = "S"  # substitution

        # backtrack
        i, j = len(word1) - 1, len(word2) - 1
        operations = []

        while i > 0 or j > 0:
            if i > 0 and j > 0 and op_matrix[i][j] == "S":
                operations.append(f"Substitute '{word1[i]}' with '{word2[j]}'")
                i -= 1
                j -= 1
            elif i > 0 and op_matrix[i][j] == "D":
                operations.append(f"Delete '{word1[i]}'")
                i -= 1
            elif j > 0 and op_matrix[i][j] == "I":
                operations.append(f"Insert '{word2[j]}'")
                j -= 1
            else:
                operations.append(f"Keep '{word2[j]}'")
                i -= 1
                j -= 1

        operations.reverse()

        score = dl_matrix[-1][-1]

        return score, operations

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
            word_chars.append(char)

        return word_chars
