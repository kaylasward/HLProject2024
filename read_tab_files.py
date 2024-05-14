import pandas as pd


class TabFileReader:
    def __init__(self):
        pass

    @staticmethod
    def get_word_list(data_df):
        df_word_list = []
        # cols
        for column in data_df.columns[1:]:
            # row
            for index in data_df.index:
                if index != 0:
                    token = data_df.at[index, column]
                    df_word_list.append(token)

        df_word_list = list(filter(None, df_word_list))

        return df_word_list

    @staticmethod
    def tab_reader(path):
        data = []
        with open(path) as cognacy_f:
            for line in cognacy_f.readlines():
                line = line[:-1].split("\t")
                data.append(line)
        return pd.DataFrame(data)

    @staticmethod
    def get_alphabet(word_list):
        # extract all letters
        letters = sorted([letter for word in word_list for letter in word])

        # extract unique
        unique_letters = set(letters)

        # sort them
        sorted_letters_string = "".join(unique_letters)

        return sorted_letters_string
