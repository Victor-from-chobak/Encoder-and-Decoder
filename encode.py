import requests
import string
import pickle
import argparse
import random
import sys


parser = argparse.ArgumentParser()
parser.add_argument('operating_mode', type=str, help='HowToOperate')
parser.add_argument('--input_url', default='NoUrl', type=str, help='input url_for_text')
parser.add_argument('--input_file', default='NoFile', type=str, help='input_file')
parser.add_argument('--output_file', default='NoFile', type=str, help='output file')
parser.add_argument('--cipher', default='NoCipher', type=str, help='Cipher for encoding')
parser.add_argument('--key', default='NoKey', type=str, help='key for encoding')
parser.add_argument('--AnalyzedDataFile', default='NoFile', type=str, help='File with frequency')
parser.add_argument('--language', default='eng', type=str, help='Language of encoding')
parser.add_argument('--random_file', default='NoFile', type=str, help='File with random string for Vernam')
myNamespace = parser.parse_args()
EnglishTextUrl = 'http://www.gutenberg.org/files/296/296-0.txt'
utfEncoding = 'utf-16le'


class TextAnalysis:

    LatinChars = string.ascii_letters + string.punctuation + string.digits + '\n' + ' ' + '”“’'
    RussianAlphabet = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    RussianChars = RussianAlphabet + string.punctuation + string.digits + '\n' + ' ' + '”“’'

    def __init__(self, text):
        self.mainText = text
        self.countLetters = dict()
        self.setOfWords = set()

    def getWords(self):
        self.setOfWords = set(self.mainText.split(' '))

    def countFrequency(self):
        for letter in self.mainText:
            if letter not in self.countLetters:
                self.countLetters[letter] = 0
            self.countLetters[letter] += 1

        Total = 0
        for letter in self.countLetters.keys():
            Total += self.countLetters[letter]

        for letter in self.countLetters.keys():
            self.countLetters[letter] /= Total

    def outFrequencyLatin(self):
        for letter in string.ascii_lowercase:
            print(self.countLetters[letter])

    def getSetOfWords(text):
        return set(text.split(' '))


class Vigenere:

    LatinIndex = 0.0644
    RussianIndex = 0.0553
    UpperBoundFor = 100
    Epsilon = 0.01

    def __init__(self, LanguageAlphabet, word):
        self.codeWord = word
        self.lenOfWord = len(word)
        self.currentIndex = 0
        self.Alphabet = LanguageAlphabet
        self.Len = len(self.Alphabet)

    def getLetter(self, char):
        letter = self.codeWord[self.currentIndex]
        indChar = self.Alphabet.find(char)
        indLetter = self.Alphabet.find(letter)
        newInd = (indChar + indLetter) % self.Len
        answerLetter = self.Alphabet[newInd]
        self.currentIndex = (self.currentIndex + 1) % self.lenOfWord
        return answerLetter

    def getAntiWord(LanguageAlphabet, word):
        answerWord = ''
        Len = len(LanguageAlphabet)
        for letter in word:
            indLetter = LanguageAlphabet.find(letter)
            newInd = (Len - indLetter) % Len
            answerWord += LanguageAlphabet[newInd]

        return answerWord

    def countIndex(text, LanguageAlphabet):
        d = dict()
        for i in LanguageAlphabet:
            d[i] = 0
        for i in text:
            d[i] += 1
        n = len(text)
        if n == 1:
            return 0
        Index = 0
        for i in d.keys():
            Index += d[i] * (d[i] - 1) / n / (n - 1)

        return Index

    def giveShiftedAlphabet(LanguageAlphabet, shift):
        answer = ''
        for i in range(len(LanguageAlphabet)):
            j = (i + shift) % len(LanguageAlphabet)
            answer += LanguageAlphabet[j]
        return answer

    def doubleIndex(text1, text2, shift, LanguageAlphabet):
        AnotherAlphabet = Vigenere.giveShiftedAlphabet(LanguageAlphabet, shift)
        d1 = dict()
        d2 = dict()
        n1 = len(text1)
        n2 = len(text2)
        for i in LanguageAlphabet:
            d1[i] = 0
            d2[i] = 0
        for j in text1:
            d1[j] += 1
        for j in text2:
            d2[j] += 1
        MIndex = 0
        for i in range(len(LanguageAlphabet)):
            letter1 = LanguageAlphabet[i]
            letter2 = AnotherAlphabet[i]
            MIndex += d1[letter1] * d2[letter2] / n1 / n2
        return MIndex

    def gcd(a, b):
        if not b:
            return a
        return Vigenere.gcd(b, a % b)

    def bigGcd(ListOfIntegers):
        if not ListOfIntegers:
            raise RuntimeError('Empty list for gcd')

        answer = ListOfIntegers[0]
        for i in range(len(ListOfIntegers) - 1):
            answer = Vigenere.gcd(answer, ListOfIntegers[i + 1])
        return answer

    def encodeText(self, text):
        answerText = ''
        for j in text:
            answerText += self.getLetter(j)
        return answerText


def getTextFromUrl(url):
    return requests.get(url).text


def LettersInFile(fileName):
    if fileName != 'NoFile':
        with open(fileName, 'r') as file:
            s = file.read()
    else:
        s = sys.stdin.read()

    return s


def writeToFile(text):
    if myNamespace.output_file == 'NoFile':
        sys.stdout.write(text)
    else:
        with open(myNamespace.output_file, 'w') as file:
            file.write(text)


def understandLanguage(text):
    setText = set(text)
    if len(setText & set(TextAnalysis.LatinChars)) > len(setText & set(TextAnalysis.RussianChars)):
        return TextAnalysis.LatinChars
    else:
        return TextAnalysis.RussianChars


def setStatistics():
    UsingText = TextAnalysis(url=myNamespace.input_url, fileName=myNamespace.input_file)
    UsingText.countFrequency()
    UsingText.getWords()
    Data = (UsingText.countLetters, UsingText.setOfWords)

    with open(myNamespace.output_file, 'wb') as file:
        pickle.dump(Data, file)


def getStatistic():
    if myNamespace.AnalyzedDataFile == 'NoFile':
        raise RuntimeError('No file with frequency')

    data = dict()

    with open(myNamespace.AnalyzedDataFile, "rb") as file:
        data = pickle.load(file)

    return data


def vectorDistance(vectorData, vectorBad, shift, LanguageAlphabet=TextAnalysis.LatinChars):
    distance = 0
    for i in range(len(LanguageAlphabet)):
        j = (i + shift) % len(LanguageAlphabet)
        key = LanguageAlphabet[j]
        if key not in vectorData:
            a = 0
        else:
            a = vectorData[key]
        if key not in vectorBad:
            b = 0
        else:
            b = vectorBad[key]

        distance += (a - b) ** 2

    return distance


def makeString(mapChar, text):
    answerText = ''
    for char in text:
        if char not in mapChar:
            answerText += char
            continue
        answerText += mapChar[char]
    return answerText


def getMovedWords(Text, shift, LanguageAlphabet=TextAnalysis.LatinChars):
    newText = ''
    for char in Text:
        if char not in LanguageAlphabet:
            newText += char
            continue
        index = LanguageAlphabet.find(char)
        newIndex = (index + shift) % len(LanguageAlphabet)
        newText += LanguageAlphabet[newIndex]
    return set(newText.split(' '))


def HackCaesar(text, LanguageAlphabet=TextAnalysis.LatinChars):
    UsingText = TextAnalysis(text)
    UsingText.countFrequency()
    GivenData = getStatistic()
    NormalFrequency = GivenData[0]
    GivenWords = GivenData[1]

    bestShift = 0
    bestDistance = 10**10
    bestCountWords = 0
    LenLanguage = len(LanguageAlphabet)

    for shift in range(LenLanguage):
        d = vectorDistance(NormalFrequency, UsingText.countLetters, shift)

        setShift = getMovedWords(UsingText.mainText, shift, LanguageAlphabet=LanguageAlphabet)
        shiftWords = len(setShift & GivenWords)

        if (shiftWords > bestCountWords) or (shiftWords == bestCountWords and d < bestDistance):
            bestShift = shift
            bestDistance = d
            bestCountWords = shiftWords

    print(LenLanguage)
    print(bestShift)
    mapEncoding = dict()
    array = list(UsingText.countLetters.keys())

    for i in range(LenLanguage):
        j = (i + bestShift) % LenLanguage
        mapEncoding[LanguageAlphabet[i]] = LanguageAlphabet[j]

    return(bestCountWords, mapEncoding)


def HackVigenere(text, LanguageAlphabet):
    GivenData = getStatistic()
    GivenWords = GivenData[1]
    EncodedText = text
    goodLen = list()
    N = len(EncodedText)
    for t in range(1, 100):
        Strings = [''] * t
        Indexes = [0] * t
        flag = True
        for i in range(t):
            j = i
            while j < N:
                Strings[i] += EncodedText[j]
                j += t
            Indexes[i] = Vigenere.countIndex(Strings[i], LanguageAlphabet)
            flag &= (abs(Indexes[i] - Vigenere.LatinIndex) < Vigenere.Epsilon)
        if flag:
            goodLen.append(t)
    keyLen = Vigenere.bigGcd(goodLen)
    Strings = [''] * keyLen
    for i in range(keyLen):
        j = i
        while j < N:
            Strings[i] += EncodedText[j]
            j += t

    MA = len(LanguageAlphabet)
    deltas = [0] * keyLen
    for i in range(keyLen - 1):
        maxInd = 0
        bestShift = 0
        for s in range(MA):
            ind = Vigenere.doubleIndex(Strings[i], Strings[i + 1], s, LanguageAlphabet)
            if ind > maxInd:
                maxInd = ind
                bestShift = s
        deltas[i] = (MA - bestShift) % MA

    bestKey = ''
    bestWords = 0

    for i in range(MA):
        tryKey = LanguageAlphabet[i]
        curIndex = i
        for j in range(keyLen - 1):
            curIndex = (curIndex + deltas[j]) % MA
            tryKey += LanguageAlphabet[curIndex]

        Encoder = Vigenere(LanguageAlphabet, tryKey)
        newText = Encoder.encodeText(EncodedText)
        newSet = TextAnalysis.getSetOfWords(newText)
        crossSet = len(newSet & GivenWords)
        if crossSet > bestWords:
            bestWords = crossSet
            bestKey = tryKey

    return (bestWords, bestKey)


def Hack():
    text = LettersInFile(myNamespace.input_file)
    flag = True
    LanguageAlphabet = understandLanguage(text)
    for char in text:
        flag &= char in LanguageAlphabet

    p1 = HackCaesar(text, LanguageAlphabet)
    if flag:
        p2 = HackVigenere(text, LanguageAlphabet)
    else:
        p2 = (-1, 0)

    if p1[0] > p2[0]:
        writeToFile(makeString(p1[1], text))
    else:
        EncodingVigenere(p2[1], LanguageAlphabet, text)


def EncodingCaesar(shift, LanguageAlphabet, text):
    Text = TextAnalysis(text)
    mapEncoding = dict()
    LenLanguage = len(LanguageAlphabet)
    shift = ((shift % LenLanguage) + LenLanguage) % LenLanguage

    for i in range(LenLanguage):
        j = (i + shift) % LenLanguage
        mapEncoding[LanguageAlphabet[i]] = LanguageAlphabet[j]

    writeToFile(makeString(mapEncoding, text))


def EncodingVigenere(word, LanguageAlphabet, text):
    Encoder = Vigenere(LanguageAlphabet, word)
    answerText = ''
    for char in text:
        if char not in LanguageAlphabet:
            answerText += char
            continue
        answerText += Encoder.getLetter(char)
    writeToFile(answerText)


def setVernamKey(LanguageAlphabet, Len):
    answerStr = ''
    random.seed()
    with open(myNamespace.random_file, 'w') as file:
        for i in range(Len):
            randomNum = random.randint(0, len(LanguageAlphabet) - 1)
            letter = LanguageAlphabet[randomNum]
            file.write(letter)
            answerStr += letter

    return answerStr


def VernamMakeOutFile(text):
    KeyString = LettersInFile(myNamespace.random_file)

    with open(myNamespace.output_file, 'wb') as file:
        x = [ord(text[i]) ^ ord(KeyString[i]) for i in range(len(text))]
        pickle.dump(x, file)


def EncodingVernam(LanguageAlphabet, text):
    if myNamespace.random_file == 'NoFile':
        raise RuntimeError('No file for random string')

    cnt = len(text) * 2
    setVernamKey(LanguageAlphabet, cnt)
    VernamMakeOutFile()


def DecodingVernam():
    if myNamespace.random_file == 'NoFile':
        raise RuntimeError('No file for random string')

    KeyString = LettersInFile(myNamespace.random_file)

    with open(myNamespace.input_file, 'rb') as file:
        ar = pickle.load(file)

    answerString = ''
    for i in range(len(ar)):
        letter = chr(ar[i] ^ ord(KeyString[i]))
        answerString += letter

    writeToFile(answerString)


def Encoding():
    if myNamespace.input_url != 'NoUrl':
        Text = getTextFromUrl(url)
    else:
        Text = LettersInFile(myNamespace.input_file)

    if myNamespace.cipher == 'NoCipher':
        raise RuntimeError('No cipher was given')

    if myNamespace.language == 'eng':
        LanguageAlphabet = TextAnalysis.LatinChars

    if myNamespace.language == 'rus':
        LanguageAlphabet = TextAnalysis.RussianChars

    if myNamespace.cipher == 'NoCipher':
        raise RuntimeError('Give a cipher')

    if myNamespace.cipher == 'caesar':
        EncodingCaesar(LanguageAlphabet=LanguageAlphabet, shift=int(myNamespace.key), text=Text)

    elif myNamespace.cipher == 'vigenere':
        EncodingVigenere(word=myNamespace.key, LanguageAlphabet=LanguageAlphabet, text=Text)

    elif myNamespace.cipher == 'vernam':
        EncodingVernam(LanguageAlphabet=LanguageAlphabet, text=Text)


def Decoding():

    if myNamespace.cipher == 'vernam':
        DecodingVernam()

    if myNamespace.input_url != 'NoUrl':
        Text = getTextFromUrl(url)
    else:
        Text = LettersInFile(myNamespace.input_file)

    if myNamespace.cipher == 'NoCipher':
        raise RuntimeError('No cipher was given')

    if myNamespace.language == 'eng':
        LanguageAlphabet = TextAnalysis.LatinChars

    elif myNamespace.language == 'rus':
        LanguageAlphabet = TextAnalysis.RussianChars

    if myNamespace.cipher == 'caesar':
        newShift = len(LanguageAlphabet) - int(myNamespace.key)
        EncodingCaesar(LanguageAlphabet=LanguageAlphabet, shift=newShift, text=Text)

    elif myNamespace.cipher == 'vigenere':
        newWord = Vigenere.getAntiWord(word=myNamespace.key, LanguageAlphabet=LanguageAlphabet)
        EncodingVigenere(word=newWord, LanguageAlphabet=LanguageAlphabet, text=Text)


def main():
    if myNamespace.operating_mode == 'read':
        setStatistics()
    elif myNamespace.operating_mode == 'hack':
        Hack()
    elif myNamespace.operating_mode == 'encode':
        Encoding()
    elif myNamespace.operating_mode == 'decode':
        Decoding()
    else:
        raise RuntimeError('Incorrect input')


main()
