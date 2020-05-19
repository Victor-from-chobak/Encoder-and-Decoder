import requests
import pickle
import argparse
import random
import sys
import typing

sys.path.append('src')

from TextAnalysis import TextAnalysis
from VigenereClass import VigenereCipher


def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('operating_mode', type=str, help='HowToOperate')
    parser.add_argument('--input_url', default=None, type=str, help='full url starts with http://')
    parser.add_argument('--input_file', default=None, type=str, help='text file in utf-8 in english/russian language')
    parser.add_argument('--output_file', default=None, type=str, help='any file')
    parser.add_argument('--cipher', default='NoCipher', type=str, help='Cipher for encoding')
    parser.add_argument('--key', default='NoKey', type=str, help='key for encoding, number for caesar, string for vigenere')
    parser.add_argument('--AnalyzedDataFile', default=None, type=str, help='File with frequency got from input file')
    parser.add_argument('--language', default='eng', type=str, help='Language of encoding', choices=['eng', 'rus'])
    parser.add_argument('--random_file', default=None, type=str, help='File with random string for Vernam')
    myNamespace = parser.parse_args()
    return myNamespace


def get_text_from_url(url):
    return requests.get(url).text


def letters_in_file(fileName):
    """[give text from file]

    Arguments:
        fileName {[str]} -- [name of file]

    Returns:
        [str] -- [text in file]
    """
    if fileName != None:
        with open(fileName, 'r') as file:
            currentString = file.read()
    else:
        currentString = sys.stdin.read()

    return currentString


def write_to_file(myNamespace, text):
    if myNamespace.output_file == None:
        sys.stdout.write(text)
    else:
        with open(myNamespace.output_file, 'w') as file:
            file.write(text)


def understand_language(text):
    """[Function for hacking]

    Arguments:
        text {[str]} -- [encoded text]

    Returns:
        [str] -- [Alphabet of current language]
    """
    setText = set(text)
    if len(setText & set(TextAnalysis.LATIN_CHARS)) > len(setText & set(TextAnalysis.RUSSIAN_CHARS)):
        return TextAnalysis.LATIN_CHARS
    else:
        return TextAnalysis.RUSSIAN_CHARS


def set_statistics(myNamespace):
    """In operating mode READ set frequency of letters in output_file"""

    if myNamespace.input_url != None:
        text = get_text_from_url(myNamespace.input_url)
    else:
        text = letters_in_file(myNamespace.input_file)

    usingText = TextAnalysis(text)
    usingText.countFrequency()
    usingText.getWords()
    data = (usingText.numberOfLetters, usingText.setOfWords)

    with open(myNamespace.output_file, 'wb') as file:
        pickle.dump(data, file)


def get_statistic(myNamespace):
    """Give statistic for hack ciphers"""

    if myNamespace.AnalyzedDataFile == None:
        raise RuntimeError('No file with frequency')

    data = dict()

    with open(myNamespace.AnalyzedDataFile, "rb") as file:
        data = pickle.load(file)

    return data


def vector_distance(vectorData, vectorBad, shift, languageAlphabet=TextAnalysis.LATIN_CHARS):
    """[using in caesar to find minimal difference between vectors]

    Arguments:
        vectorData {[dict]} -- [normal vector]
        vectorBad {[dict]} -- [encoded vector]
        shift {[int]} -- [shift in caesar]

    Keyword Arguments:
        languageAlphabet {[type]} -- [] (default: {TextAnalysis.LATIN_CHARS})

    Returns:
        [float] -- [distance between vectors]
    """
    distance = 0
    for i in range(len(languageAlphabet)):
        j = (i + shift) % len(languageAlphabet)
        key = languageAlphabet[j]
        if key not in vectorData:
            firstCordinate = 0
        else:
            firstCordinate = vectorData[key]
        if key not in vectorBad:
            secondCordinate = 0
        else:
            secondCordinate = vectorBad[key]

        distance += (firstCordinate - secondCordinate) ** 2

    return distance


def make_string(mapChar, text):
    """[encode/decode given text]

    Arguments:
        mapChar {[dict]} -- [description]
        text {[str]} -- [description]

    Returns:
        [str] -- [encoded/decoded text]
    """
    answerText = ''
    for char in text:
        if char not in mapChar:
            answerText += char
            continue
        answerText += mapChar[char]
    return answerText


def get_moved_words(text, shift, languageAlphabet=TextAnalysis.LATIN_CHARS):
    """encoded/decoded words from caesar cipher"""
    newText = ''
    for char in text:
        if char not in languageAlphabet:
            newText += char
            continue
        index = languageAlphabet.find(char)
        newIndex = (index + shift) % len(languageAlphabet)
        newText += languageAlphabet[newIndex]
    return set(newText.split(' '))


def hack_caesar_cipher(myNamespace, text, languageAlphabet=TextAnalysis.LATIN_CHARS):
    """[main function to hack caesar]

    Arguments:
        text {[str]} -- [encoded text]

    Keyword Arguments:
        languageAlphabet {[str]} -- [current alphabet] (default: {TextAnalysis.LATIN_CHARS})

    Returns:
        [tuple] -- [pair of count of normal words and dict for decoding]
    """
    usingText = TextAnalysis(text)
    usingText.countFrequency()
    givenData = get_statistic(myNamespace)
    normalFrequency = givenData[0]
    givenWords = givenData[1]

    bestShift = 0
    bestDistance = 10**10
    bestCountWords = 0
    lenLanguage = len(languageAlphabet)

    for shift in range(lenLanguage):
        curDist = vector_distance(normalFrequency, usingText.numberOfLetters, shift)

        setShift = get_moved_words(usingText.mainText, shift, languageAlphabet=languageAlphabet)
        shiftWords = len(setShift & givenWords)

        if (shiftWords > bestCountWords) or (shiftWords == bestCountWords and curDist < bestDistance):
            bestShift = shift
            bestDistance = curDist
            bestCountWords = shiftWords

    mapEncoding = dict()
    array = list(usingText.numberOfLetters.keys())

    for i in range(lenLanguage):
        j = (i + bestShift) % lenLanguage
        mapEncoding[languageAlphabet[i]] = languageAlphabet[j]

    return(bestCountWords, mapEncoding)


def count_key_len_for_Vigenere(encodedText, languageAlphabet):
    """[help hack_vigenere_cipher to calculate len of key]

    Arguments:
        encodedText {[str]} -- [given text]
        languageAlphabet {[str]} -- [current alphabet]

    Returns:
        [int] -- [len of the key]
    """
    goodLen = list()
    lenText = len(encodedText)
    for t in range(1, 100):
        Strings = [''] * t
        Indexes = [0] * t
        flag = True
        for i in range(t):
            j = i
            while j < lenText:
                Strings[i] += encodedText[j]
                j += t
            Indexes[i] = VigenereCipher.count_index(Strings[i], languageAlphabet)
            flag &= (abs(Indexes[i] - VigenereCipher.LATIN_INDEX) < VigenereCipher.EPSILON)
        if flag:
            goodLen.append(t)
    return VigenereCipher.big_gcd(goodLen)


def hack_vigenere_cipher(myNamespace, text, languageAlphabet):
    """[Main function for hack vigenere cipher]

    Arguments:
        text {[str]} -- [encoded text]
        languageAlphabet {[str]} -- [current alphabet]

    Returns:
        [tuple] -- [pair of count of normal words and key of cipher]
    """

    givenData = get_statistic(myNamespace)
    givenWords = givenData[1]
    encodedText = text
    lenText = len(encodedText)
    try:
        keyLen = count_key_len_for_Vigenere(encodedText, languageAlphabet)
    except RuntimeError:
        return (-1, 0)
    strings = [''] * keyLen
    for i in range(keyLen):
        j = i
        while j < lenText:
            strings[i] += encodedText[j]
            j += keyLen

    lenLan = len(languageAlphabet)
    deltas = [0] * keyLen
    for i in range(keyLen - 1):
        maxInd = 0
        bestShift = 0
        for s in range(lenLan):
            ind = VigenereCipher.get_index_overlap_two_strings(strings[i], strings[i + 1], s, languageAlphabet)
            if ind > maxInd:
                maxInd = ind
                bestShift = s
        deltas[i] = (lenLan - bestShift) % lenLan

    bestKey = ''
    bestWords = 0

    for i in range(lenLan):
        tryKey = languageAlphabet[i]
        curIndex = i
        for j in range(keyLen - 1):
            curIndex = (curIndex + deltas[j]) % lenLan
            tryKey += languageAlphabet[curIndex]

        encoder = VigenereCipher(languageAlphabet, tryKey)
        newText = encoder.encode_text(encodedText)
        newSet = TextAnalysis.getSetOfWords(newText)
        crossSet = len(newSet & givenWords)
        if crossSet > bestWords:
            bestWords = crossSet
            bestKey = tryKey

    return (bestWords, bestKey)


def Hack(myNamespace):
    """This function try to hack text such as encoded as caesar and vigenere"""
    text = letters_in_file(myNamespace.input_file)
    flag = True
    languageAlphabet = understand_language(text)
    for char in text:
        flag &= char in languageAlphabet

    firstPair = hack_caesar_cipher(myNamespace, text, languageAlphabet)
    if flag:
        secondPair = hack_vigenere_cipher(myNamespace, text, languageAlphabet)
    else:
        secondPair = (-1, 0)

    if firstPair[0] > secondPair[0]:
        write_to_file(myNamespace, make_string(firstPair[1], text))
    else:
        encoding_vigenere(secondPair[1], languageAlphabet, text, myNamespace)


def encoding_caesar(shift, languageAlphabet, text, myNamespace):
    mapEncoding = dict()
    LenLanguage = len(languageAlphabet)
    shift = ((shift % LenLanguage) + LenLanguage) % LenLanguage

    for i in range(LenLanguage):
        j = (i + shift) % LenLanguage
        mapEncoding[languageAlphabet[i]] = languageAlphabet[j]

    write_to_file(myNamespace, make_string(mapEncoding, text))


def encoding_vigenere(word, languageAlphabet, text, myNamespace):
    encoder = VigenereCipher(languageAlphabet, word)
    answerText = ''
    for char in text:
        if char not in languageAlphabet:
            answerText += char
            continue
        answerText += encoder.get_letter(char)
    write_to_file(myNamespace, answerText)


def set_vernam_key(languageAlphabet, Len, myNamespace):
    """make string for vernam cipher"""

    answerStr = ''
    random.seed()
    with open(myNamespace.random_file, 'w') as file:
        for i in range(Len):
            randomNum = random.randint(0, len(languageAlphabet) - 1)
            letter = languageAlphabet[randomNum]
            file.write(letter)
            answerStr += letter

    return answerStr


def vernam_make_out_file(text, myNamespace):
    keyString = letters_in_file(myNamespace.random_file)

    with open(myNamespace.output_file, 'wb') as file:
        tempList = [ord(text[i]) ^ ord(keyString[i]) for i in range(len(text))]
        pickle.dump(tempList, file)


def encoding_vernam(languageAlphabet, text, myNamespace):
    if myNamespace.random_file == None:
        raise RuntimeError('No file for random string')

    cnt = len(text) * 2
    set_vernam_key(languageAlphabet, cnt, myNamespace)
    vernam_make_out_file(text, myNamespace)


def decoding_vernam(myNamespace):
    if myNamespace.random_file == None:
        raise RuntimeError('No file for random string')

    KeyString = letters_in_file(myNamespace.random_file)

    with open(myNamespace.input_file, 'rb') as file:
        array = pickle.load(file)

    answerString = ''
    for i in range(len(array)):
        letter = chr(array[i] ^ ord(KeyString[i]))
        answerString += letter

    write_to_file(myNamespace, answerString)


def Encoding(myNamespace):
    """This function handle work of encoding"""

    if myNamespace.input_url != None:
        text = get_text_from_url(url)
    else:
        text = letters_in_file(myNamespace.input_file)

    if myNamespace.cipher == 'NoCipher':
        raise RuntimeError('No cipher was given')

    if myNamespace.language == 'eng':
        languageAlphabet = TextAnalysis.LATIN_CHARS

    if myNamespace.language == 'rus':
        languageAlphabet = TextAnalysis.RUSSIAN_CHARS

    if myNamespace.cipher == 'NoCipher':
        raise RuntimeError('Give a cipher')

    if myNamespace.cipher == 'caesar':
        encoding_caesar(languageAlphabet=languageAlphabet, shift=int(myNamespace.key), text=text, myNamespace=myNamespace)

    elif myNamespace.cipher == 'vigenere':
        encoding_vigenere(word=myNamespace.key, languageAlphabet=languageAlphabet, text=text, myNamespace=myNamespace)

    elif myNamespace.cipher == 'vernam':
        encoding_vernam(languageAlphabet=languageAlphabet, text=text, myNamespace=myNamespace)


def Decoding(myNamespace):
    """This function handle work of decoding"""

    if myNamespace.cipher == 'vernam':
        decoding_vernam(myNamespace)
        return 0

    if myNamespace.input_url != None:
        text = get_text_from_url(url)
    else:
        text = letters_in_file(myNamespace.input_file)

    if myNamespace.cipher == 'NoCipher':
        raise RuntimeError('No cipher was given')

    if myNamespace.language == 'eng':
        languageAlphabet = TextAnalysis.LATIN_CHARS

    elif myNamespace.language == 'rus':
        languageAlphabet = TextAnalysis.RUSSIAN_CHARS

    if myNamespace.cipher == 'caesar':
        newShift = len(languageAlphabet) - int(myNamespace.key)
        encoding_caesar(languageAlphabet=languageAlphabet, shift=newShift, text=text, myNamespace=myNamespace)

    elif myNamespace.cipher == 'vigenere':
        newWord = VigenereCipher.get_anti_word(word=myNamespace.key, languageAlphabet=languageAlphabet)
        encoding_vigenere(word=newWord, languageAlphabet=languageAlphabet, text=text, myNamespace=myNamespace)


def main():
    myNamespace = parsing()

    if myNamespace.operating_mode == 'read':
        set_statistics(myNamespace)
    elif myNamespace.operating_mode == 'hack':
        Hack(myNamespace)
    elif myNamespace.operating_mode == 'encode':
        Encoding(myNamespace)
    elif myNamespace.operating_mode == 'decode':
        Decoding(myNamespace)
    else:
        raise RuntimeError('Incorrect input')


if __name__ == '__main__':
    main()
