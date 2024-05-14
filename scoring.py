import pandas as pd

class Scoring:
    def __init__(self, scorelist, goldfile, threshold=4):
        self.goldfile = goldfile
        self.scorelist = scorelist
        self.threshold = threshold

    def transform_scorelist(self):
        gen_cognates = dict()
        for concept in self.scorelist:
            true_cognates = []
            cognates = concept['cognates']
            print("New concept!")
            for cognate_pair in cognates:
                if cognate_pair['score'] <= self.threshold:
                    true_cognates.append('?') # Here, I would like to add info on what column the words come from
                    # However, the score list does not contain info of whoch column/language the concept is from,
                    # only the form
            concept_name = concept['EnglishWord']
            gen_cognates[concept_name] = true_cognates
        print(gen_cognates)

    
    def iterate_over_goldtable(self):
        for row in range(len(self.goldfile)):
            for col in range(len(self.goldfile.loc[row])-1):
                if row != 0 and col != 0:
                    word = self.goldfile.loc[row, col]
                    #if self.goldfile.loc[row, col] == self.goldfile.loc[row, col+1]:
                    # How to save the cognacy data?
