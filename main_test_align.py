from alignment_calculator import AlignCalculator


ac = AlignCalculator()

word1 = "hamburger"
word2 = "hammer"

score, w1, w2 = ac.global_alignment(word1, word2)
print(score)
print(w1)
print(w2)
