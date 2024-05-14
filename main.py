from calculations import CalcEdit
from read_tab_files import TabFileReader


barb_cognacy = TabFileReader.tab_reader(
    "chl2024_barbacoandata/chl2023_barbacoan_cognacy.tab"
)
barb_forms = TabFileReader.tab_reader(
    "chl2024_barbacoandata/chl2023_barbacoan_forms.tab"
)

eau_cognacy = TabFileReader.tab_reader(
    "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_cognacy.tab"
)
eau_forms = TabFileReader.tab_reader(
    "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_forms.tab"
)

ie_cognacy = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_cognacy.tab")
ie_forms = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_forms.tab")

df_word_list = TabFileReader.get_word_list(barb_forms)
alphabet = TabFileReader.get_alphabet(df_word_list)

calcedit = CalcEdit(df_word_list, alphabet)

x = calcedit.is_cognate_("su", threshold=1)

print()
print("ANSWER")
for row in x:
    print(row)
