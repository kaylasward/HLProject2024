from calculations import CalcEdit
from read_tab_files import ie_cognacy

word_list = ["casa", "house", "casa", "haus", "maison", "hamburger", "hus"]
alphabet = "abcdefghijklmnopqrstuvwxyz"

calcedit = CalcEdit(word_list, alphabet)
x = calcedit.is_cognate_("haus", threshold=4)

print()
print("ANSWER")
for row in x:
    print(row)
