class VigenereCipher:
    LATIN_INDEX = 0.0644 # Constants for hacking, got from wikipedia
    RUSSIAN_INDEX = 0.0553
    RUSSIAN_BOUND_FOR = 100
    EPSILON = 0.01

    def __init__(self, languageAlphabet, word):
        self.codeWord = word
        self.lenOfWord = len(word)
        self.currentIndex = 0
        self.Alphabet = languageAlphabet
        self.Len = len(self.Alphabet)

    def get_letter(self, char):
        """[help for decoding/encoding each letter]

        Arguments:
            char {[str]} -- [current letter]

        Returns:
            [str] -- [encoded/decoded letter]
        """
        if not self.lenOfWord:
            return char
        letter = self.codeWord[self.currentIndex]
        indChar = self.Alphabet.find(char)
        indLetter = self.Alphabet.find(letter)
        newInd = (indChar + indLetter) % self.Len
        answerLetter = self.Alphabet[newInd]
        self.currentIndex = (self.currentIndex + 1) % self.lenOfWord
        return answerLetter

    @staticmethod
    def get_anti_word(languageAlphabet, word):
        """get word for decoding"""
        answerWord = ''
        Len = len(languageAlphabet)
        for letter in word:
            indLetter = languageAlphabet.find(letter)
            newInd = (Len - indLetter) % Len
            answerWord += languageAlphabet[newInd]

        return answerWord

    @staticmethod
    def count_index(text, languageAlphabet):
        """index of single string"""
        tempDict = dict()
        for i in languageAlphabet:
            tempDict[i] = 0
        for i in text:
            tempDict[i] += 1
        lenText = len(text)
        if lenText == 1 or not lenText:
            return 0
        index = 0
        for i in d.keys():
            index += tempDict[i] * (tempDict[i] - 1) / lenText / (lenText - 1)

        return index

    @staticmethod
    def give_shifted_alphabet(languageAlphabet, shift):
        answer = ''
        for i in range(len(languageAlphabet)):
            newI = (i + shift) % len(languageAlphabet)
            answer += languageAlphabet[newI]
        return answer

    @staticmethod
    def get_index_overlap_two_strings(text1, text2, shift, languageAlphabet):
        """[for hack vigenere it count index overlap]

        Arguments:
            text1 {[str]} -- [first text]
            text2 {[str]} -- [second text]
            shift {[int]} -- []
            languageAlphabet {[str]} -- [Alphabet of current language]

        Returns:
            [float] -- [needed index]
        """
        anotherAlphabet = VigenereCipher.give_shifted_alphabet(languageAlphabet, shift)
        firstDict = dict()
        secondDict = dict()
        num1 = len(text1)
        num2 = len(text2)
        for i in languageAlphabet:
            firstDict[i] = 0
            secondDict[i] = 0
        for j in text1:
            firstDict[j] += 1
        for j in text2:
            secondDict[j] += 1
        mIndex = 0
        for i in range(len(languageAlphabet)):
            letter1 = languageAlphabet[i]
            letter2 = anotherAlphabet[i]
            mIndex += firstDict[letter1] * secondDict[letter2] / num1 / num2
        return mIndex

    @staticmethod
    def gcd(a, b):
        if not b:
            return a
        return VigenereCipher.gcd(b, a % b)

    @staticmethod
    def big_gcd(ListOfIntegers):
        if not ListOfIntegers:
            raise RuntimeError('Empty list for gcd')

        answer = ListOfIntegers[0]
        for i in range(len(ListOfIntegers) - 1):
            answer = VigenereCipher.gcd(answer, ListOfIntegers[i + 1])
        return answer

    def encode_text(self, text):
        answerText = ''
        for j in text:
            answerText += self.get_letter(j)
        return answerText
