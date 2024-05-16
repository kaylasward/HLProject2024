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
        return gen_cognates

    def transform_goldtable(self):
        """Transforms the gold df into a dict {concept: lst of pairs that are cognates}.
        A problem we still need to solve is transitivity - if a,b and b,c are cognates, a,c are too
        """
        gold_cognates = dict()
        for row in range(len(self.goldfile)):
            if row != 0:
                cognates = self.goldfile.loc[row][1:]
                cognate_set = set(cognates)
                true_cognates = []
                for w in cognates:
                    for i, unique in enumerate(cognate_set):
                        if w == "":
                            true_cognates.append(0) # to mark missing words
                        elif w == unique:
                            true_cognates.append(i) # the index of the cognate class
                gold_cognates[self.goldfile.loc[row, 0]] = true_cognates
        return gold_cognates

if __name__ == '__main__':
    from main import ie_cognacy
    scoring = Scoring(ie_cognacy, ie_cognacy)
    print(scoring.transform_goldtable())