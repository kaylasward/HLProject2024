import pandas as pd
from read_tab_files import TabFileReader

class Scoring:
    def __init__(self, cognacy_matrix, goldfile):
        self.goldfile = goldfile
        self.cognacy_matrix = cognacy_matrix

    def pairwise_cognacy(self):
        for row in range(len(self.goldfile)):
            for col in range(len(self.goldfile.loc[row])-1):
                if row != 0 and col != 0:
                    #print(self.goldfile.loc[row, col])
                    if self.goldfile.loc[row, col] == self.goldfile.loc[row, col+1]:
                        # How to save the cognacy data?



if __name__ == '__main__':
    ie_cognacy = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_cognacy.tab")
    scoring_ie = Scoring(ie_cognacy, ie_cognacy)
    scoring_ie.accuracy(scoring_ie)