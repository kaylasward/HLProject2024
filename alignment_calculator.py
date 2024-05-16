class AlignCalculator:
    def __init__(self):
        pass

    def global_alignment(
        self,
        input_word1,
        input_word2,
        match_penalty=1,
        mismatch_penalty=-1,
        gap_penalty=-2,
    ):
        """
        Determines the global alignment and score using the Needleman-Wunsch algorithm.

        Args:
            input_word1 (str): First word for comparison.
            input_word2 (str): Second word for comparison.
            match_penalty (int): Penalty cost for when characters match.
            mismatch_penalty (int): Penalty cost for when characters don't match.
            gap_penalty (int): Penalty cost for an insertion or deletion.

        Returns:
            (int) score
            (str) word1's alignment
            (str) word2's alignment
        """
        word1 = [""]
        word2 = [""]

        word1.extend(self.__deconstruct_str(input_word1))
        word2.extend(self.__deconstruct_str(input_word2))

        n, m = len(word1), len(word2)
        nw_matrix = [[0] * m for _ in range(n)]

        # init first row
        for i in range(n):
            nw_matrix[i][0] = nw_matrix[i - 1][0] + gap_penalty

        # init first column
        for j in range(m):
            nw_matrix[0][j] = nw_matrix[0][j - 1] + gap_penalty

        for i in range(1, n):
            for j in range(1, m):
                if word1[i] == word2[j]:
                    diag = nw_matrix[i - 1][j - 1] + match_penalty  # chars match
                else:
                    diag = nw_matrix[i - 1][j - 1] + mismatch_penalty  # char mismatch
                top = nw_matrix[i - 1][j] + gap_penalty  # delete from word1
                left = nw_matrix[i][j - 1] + gap_penalty  # insert from word2

                nw_matrix[i][j] = max(diag, top, left)

        # traceback
        aligned1, aligned2 = [], []
        i, j = n - 1, m - 1
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                diag = nw_matrix[i - 1][j - 1]
            if i > 0:
                top = nw_matrix[i - 1][j]
            if j > 0:
                left = nw_matrix[i][j - 1]

            # chars match or mismatch
            if i > 0 and j > 0 and (word1[i] == word2[j] or diag >= max(top, left)):
                aligned1.append(word1[i])
                aligned2.append(word2[j])
                i -= 1
                j -= 1
            # delete from word1
            elif i > 0 and (j == 0 or top >= left):
                aligned1.append(word1[i])
                aligned2.append("-")
                i -= 1
            # insert to word1
            elif j > 0:
                aligned1.append("-")
                aligned2.append(word2[j])
                j -= 1

        # if anything left over in i or j, fill with gaps
        while i > 0:
            aligned1.append(word1[i])
            aligned2.append("-")
            i -= 1
        while j > 0:
            aligned1.append("-")
            aligned2.append(word2[j])
            j -= 1

        aligned1.reverse()
        aligned2.reverse()

        return nw_matrix[n - 1][m - 1], "".join(aligned1), "".join(aligned2)

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
