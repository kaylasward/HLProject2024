import pandas as pd

def tab_reader(path):
    data = []
    with open(path) as cognacy_f:
        for line in cognacy_f.readlines():
            line = line[:-1].split('\t')
            data.append(line)
    return pd.DataFrame(data)

barb_cognacy = tab_reader('chl2024_barbacoandata/chl2023_barbacoan_cognacy.tab')
barb_forms = tab_reader('chl2024_barbacoandata/chl2023_barbacoan_forms.tab')

eau_cognacy = tab_reader('chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_cognacy.tab')
eau_forms = tab_reader('chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_forms.tab')

ie_cognacy = tab_reader('chl2024_iedata/chl2023_iedata_cognacy.tab')
ie_forms = tab_reader('chl2024_iedata/chl2023_iedata_forms.tab')

if __name__ == "__main__":
    print(barb_cognacy.loc[[0,1,2]])
    print()
    print(barb_forms.loc[[0,1,2]])