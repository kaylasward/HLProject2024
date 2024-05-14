import pandas as pd

class Scoring:
    def __init__(self, cognacy_matrix, goldfile, threshold=4):
        self.goldfile = goldfile
        self.cognacy_matrix = cognacy_matrix
        self.threshold = threshold

    def iterate_over_scoretable(self):
        for concept in self.cognacy_matrix:
            cognates = concept['cognates']
            print("New concept!")
            for cognate_pair in cognates:
                if cognate_pair['score'] <= self.threshold:

    
    def iterate_over_goldtable(self):
        for row in range(len(self.goldfile)):
            for col in range(len(self.goldfile.loc[row])-1):
                if row != 0 and col != 0:
                    word = self.goldfile.loc[row, col]
                    #if self.goldfile.loc[row, col] == self.goldfile.loc[row, col+1]:
                    # How to save the cognacy data?
