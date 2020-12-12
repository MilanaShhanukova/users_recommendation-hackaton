from pymorphy2 import MorphAnalyzer



morph = MorphAnalyzer()
word = morph.parse("разработчиком")[0].normal_form

print(word)