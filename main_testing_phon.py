from levenshtein_dist_calc import LevenshteinDistanceCalculator
import panphon


from read_tab_files import TabFileReader


# def segment_word(ft, word):
#     # This function attempts to convert plain text to IPA
#     # Since this isn't trivial and might require language-specific logic,
#     # consider this a placeholder; you might need a more accurate method.
#     ipa = ft.transliterate(word)
#     return ipa


# ft = panphon.FeatureTable()
# word1_ipa = segment_word(ft, "haus")
# word2_ipa = segment_word(ft, "house")
# print("IPA for haus:", word1_ipa)
# print("IPA for house:", word2_ipa)


barb_forms = TabFileReader.tab_reader(
    "chl2024_barbacoandata/chl2023_barbacoan_forms.tab"
)

word_list = TabFileReader.get_word_list(barb_forms)


# word_list = ["haus", "house", "maison", "casa", "hamburger"]
alphabet = "abcdefghijklmnopqrstuvwxyz"

word1 = "tsarɨp"
word2 = "tatsip"


ldc = LevenshteinDistanceCalculator(barb_forms, alphabet)
distance, operations = ldc.calculate_dl_distance(word1, word2)
print("Distance:", distance)
print("Operations:", operations)


phonetic_calculator = LevenshteinDistanceCalculator(
    barb_forms, alphabet, use_phonetic=True
)
distance, operations = phonetic_calculator.calculate_dl_distance(word1, word2)
print("Distance:", distance)
print("Operations:", operations)
