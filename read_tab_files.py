import pandas as pd


class TabFileReader:
    def __init__(self):
        pass

    @staticmethod
    def tab_reader(path):
        data = []
        with open(path) as cognacy_f:
            for line in cognacy_f.readlines():
                line = line[:-1].split("\t")
                data.append(line)
        return pd.DataFrame(data)
