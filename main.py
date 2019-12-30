import json
import os
import random
import requests
import threading

passwords = []
suffix = []

_debug = '[{"id":0,"word":"mentioner"},{"id":0,"word":"symptom"},{"id":0,"word":"one-year-old"}]'

def getWords():
    with open('api.json','r') as file: 
        jsonString = json.load(file)
        API_KEY = jsonString.get('key')
        file.close()

    requestURL = 'https://api.wordnik.com/v4/words.json/randomWords?hasDictionaryDef=true&includePartOfSpeech=noun%2Cadjective%2Cverb&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1&limit=3&api_key={}'.format(API_KEY)
    response = requests.get(requestURL)
    if response.status_code == 200:
        response = response.text
        for wordDict in json.loads(response):
            try:
                word = str(wordDict.get('word'))
            except:
                raise Exception('Unknown Dict {}'.format(wordDict))
            if '-' in word:
                passwords.append(''.join([(wordPart.capitalize()) for wordPart in word.split('-')]))
            else:
                passwords.append(word.capitalize())
    else:
        issue = response.reason
        raise Exception('Response code: {}, Message: {}'.format(response.status_code,issue))

    random.shuffle(passwords)

def getSuffix(chars=None):
    if chars is None:
        specialChars = input('Input special character(s): ').strip()
    else:
        specialChars = chars
    specialChars += str(random.randint(0,9))
    specialChars = [char for char in specialChars]
    random.shuffle(specialChars)
    suffix.extend(specialChars)

def getPasswordThreaded(chars=None):
    threads = (threading.Thread(target=getWords()),threading.Thread(target=getSuffix(chars=chars)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    password= ''.join(passwords)+''.join(suffix)

    print(password)
    addToClipBoard(password)

def getPasswordSequential(chars=None):
    getWords()
    getSuffix(chars=chars)
    password= ''.join(passwords)+''.join(suffix)

    print(password)
    addToClipBoard(password)

def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)

getPasswordThreaded()
