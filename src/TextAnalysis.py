import string


class TextAnalysis:

    ENGLISH_TEXT_URL = 'http://www.gutenberg.org/files/296/296-0.txt'
    LATIN_CHARS = string.ascii_letters + string.punctuation + string.digits + '\n' + ' ' + '”“’—'
    RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    RUSSIAN_CHARS = RUSSIAN_ALPHABET + string.punctuation + string.digits + '\n' + ' ' + '”“’'

    def __init__(self, text):
        self.mainText = text
        self.numberOfLetters = dict()
        self.setOfWords = set()

    def getWords(self):
        self.setOfWords = set(self.mainText.split(' '))

    def countFrequency(self):
        for letter in self.mainText:
            if letter not in self.numberOfLetters:
                self.numberOfLetters[letter] = 0
            self.numberOfLetters[letter] += 1

        total = 0
        for letter in self.numberOfLetters.keys():
            total += self.numberOfLetters[letter]

        for letter in self.numberOfLetters.keys():
            self.numberOfLetters[letter] /= total

    def outFrequencyLatin(self):
        for letter in string.ascii_lowercase:
            print(self.numberOfLetters[letter])

    @staticmethod
    def getSetOfWords(text):
        return set(text.split(' '))
