import pandas as pd

class Scoring:
    def __init__(self, cognacy_matrix, goldfile, threshold=4):
        self.goldfile = goldfile
        self.cognacy_matrix = cognacy_matrix
        self.threshold = threshold

    def accuracy(self):
        for concept in self.cognacy_matrix:
            for cognates in concept:
                print(cognates)
    
    def gold_table(self):
        for row in range(len(self.goldfile)):
            for col in range(len(self.goldfile.loc[row])-1):
                if row != 0 and col != 0:
                    word = self.goldfile.loc[row, col]
                    #if self.goldfile.loc[row, col] == self.goldfile.loc[row, col+1]:
                    # How to save the cognacy data?
    




if __name__ == '__main__':
    from read_tab_files import TabFileReader
    from main import score_list
    ie_cognacy = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_cognacy.tab")
    ie_scoring = Scoring(ie_cognacy, score_list)
    ie_scoring.accuracy()