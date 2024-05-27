from levenshtein_dist_calc import LevenshteinDistanceCalculator
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

#####

ie_word_list = TabFileReader.get_word_list(ie_forms)
ie_alphabet = TabFileReader.get_alphabet(ie_word_list)
ie_calcedit = LevenshteinDistanceCalculator(ie_forms, ie_alphabet)
ie_score_list = ie_calcedit.get_all_dl_distances()
ie_distance_matrices = ie_calcedit.get_distance_matrices()

eau_word_list = TabFileReader.get_word_list(eau_forms)
eau_alphabet = TabFileReader.get_alphabet(eau_word_list)
eau_calcedit = LevenshteinDistanceCalculator(eau_forms, eau_alphabet)
eau_score_list = eau_calcedit.get_all_dl_distances()
eau_distance_matrices = eau_calcedit.get_distance_matrices()

barb_word_list = TabFileReader.get_word_list(barb_forms)
barb_alphabet = TabFileReader.get_alphabet(barb_word_list)
barb_calcedit = LevenshteinDistanceCalculator(barb_forms, barb_alphabet)
barb_score_list = barb_calcedit.get_all_dl_distances()
barb_distance_matrices = barb_calcedit.get_distance_matrices()

print(barb_distance_matrices[0])
print(barb_score_list)

#####

from scoring import Scoring

ie_scoring = Scoring(ie_score_list, ie_cognacy)
# ie_scoring.iterate_over_goldtable()
