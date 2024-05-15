import pandas as pd


class Scoring:
    def __init__(self, scorelist, goldfile, threshold=4):
        self.goldfile = goldfile
        self.scorelist = scorelist
        self.threshold = threshold

    def transform_scorelist(self):
        """This function is supposed to transform the scorelist into a dictionary with
        concept: list of pairs that are cognates. It doesn't work yet."""
        gen_cognates = dict()
        for concept in self.scorelist:
            true_cognates = []
            cognates = concept["cognates"]
            print("New concept!")
            for cognate_pair in cognates:
                if cognate_pair["score"] <= self.threshold:
                    true_cognates.append(
                        "?"
                    )  # Here, I would like to add info on what column the words come from
                    # However, the score list does not contain info of whoch column/language the concept is from,
                    # only the form
            concept_name = concept["lexeme"]
            gen_cognates[concept_name] = true_cognates
        print(gen_cognates)
        return gen_cognates

    def transform_goldtable(self):
        """Transforms the gold df into a dict {concept: lst of pairs that are cognates}.
        A problem we still need to solve is transitivity - if a,b and b,c are cognates, a,c are too
        """
        gold_cognates = dict()
        for row in range(len(self.goldfile)):
            true_cognates = []
            for col in range(len(self.goldfile.loc[row]) - 1):
                if row != 0 and col != 0:
                    if self.goldfile.loc[row, col] == self.goldfile.loc[row, col + 1]:
                        true_cognates.append((col, col + 1))
                    gold_cognates[row] = true_cognates
        print(gold_cognates)
        return gold_cognates
