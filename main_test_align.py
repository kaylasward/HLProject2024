from alignment_calculator import AlignCalculator


ac = AlignCalculator()

word1 = "hamburger"
word2 = "hammer"

score, w1, w2 = ac.global_alignment(word1, word2)
print("Global score:", score)
print(w1)
print(w2)

print("")
score, matching_segment, w1, w2aligned = ac.local_alignment(word1, word2)
print("Local score:", score)
print("Segment:", matching_segment)
print(w1)
print(w2aligned)
