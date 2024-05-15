from levenshtein_dist_calc import LevenshteinDistanceCalculator
from levenshtein_phonetic_dist_calc import LevenshteinPhoneticDistanceCalculator


word_list = ["haus", "house", "maison", "casa", "hamburger"]
alphabet = "abcdefghijklmnopqrstuvwxyz"

ldc = LevenshteinDistanceCalculator(alphabet)
distance, operations = ldc.calculate_dl_distance("haus", "house")
print("Distance:", distance)
print("Operations:", operations)


phonetic_calculator = LevenshteinPhoneticDistanceCalculator(alphabet)
distance, operations = phonetic_calculator.calculate_dl_distance("haus", "house")
print("Distance:", distance)
print("Operations:", operations)
