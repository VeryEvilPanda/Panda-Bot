import googletrans

languages = []

for i in googletrans.LANGUAGES:
    languages.append(googletrans.LANGUAGES[i])

print(languages)