import nltk
import os
import json
from imutils import paths
from nltk.stem.snowball import FrenchStemmer

def defaultValues():
    subjects=[]
    types=[]
    dictionnary= {}
    nbrStopWord= 42
    subjects, types, dictionnary= readPath("training_data", subjects, types, dictionnary)
    subjects, types, dictionnary= readPath("plugins", subjects, types, dictionnary)
    myList= dictionnaryToList(dictionnary)
    myList.sort(key=lambda tup: tup[1], reverse=True)
    stopwords=[]
    for word in myList[0:nbrStopWord-1]:
        stopwords.append(word[0])
    dictionnary= []
    for word in myList[nbrStopWord-1:-1]:
        dictionnary.append(word[0])
    return subjects, types, stopwords, dictionnary

def readPath(pathName, subjects, types, dictionnary):
    trainingPaths = list(paths.list_files(pathName, validExts="json"))
    #print(trainingPaths)
    for (i, trainingPath) in enumerate(trainingPaths):
        name = trainingPath.split(os.path.sep)[-2]
        filname = trainingPath.split(os.path.sep)[-1]
        themeName= filname.split(".")[0]
        if pathName == "plugins":
            themeName= name
        if pathName == "plugins" and filname != "intents.json" :
            continue
        with open(trainingPath, encoding="utf-8") as trainingFile:
            dataTraining= json.load(trainingFile)
            subjects, types, dictionnary= parseFileData(dataTraining, themeName, subjects, types, dictionnary)
    return subjects, types, dictionnary
    
def parseFileData(dataList, themeName, subjects, types, dictionnary):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stemmer = FrenchStemmer()
    for data in dataList:
        subject= themeName+"."+data["subject"]
        if subject not in subjects :
            subjects.append(subject)
        if data["type"] not in types:
            types.append(data["type"])
        sentences = data["sentences"] + data["responses"]
        for sentence in sentences:
            tokens= tokenizer.tokenize(sentence)
            for token in tokens:
                word= stemmer.stem(token.lower())
                if token in dictionnary :
                    dictionnary[word]+=1
                else:
                    dictionnary[word]=1
    return subjects, types, dictionnary

def dictionnaryToList(myDictionary):
    dictList=[]
    for key in myDictionary:
        dictList.append((key,myDictionary[key]))
    return dictList

def bagOfWords(sentence, dictionnary, stopwords):
    bag = [0 for _ in range(len(dictionnary))]
    sNormalized= normalize(sentence, stopwords)
    for i in range(len(bag)):
        if dictionnary[i] in sNormalized:
            bag[i]=1
    return bag

def normalize(sentence, stopwords):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stemmer = FrenchStemmer()
    tokens= tokenizer.tokenize(sentence)
    values= []
    for token in tokens:
        word= stemmer.stem(token.lower())
        if word not in stopwords:
            values.append(word)
    return values

def readPathForTraining(pathName, subjects, types, dictionnary, stopwords):
    input=[]
    outputS=[]
    outputT=[]
    outputV=[]
    trainingPaths = list(paths.list_files(pathName, validExts="json"))
    for (i, trainingPath) in enumerate(trainingPaths):
        name = trainingPath.split(os.path.sep)[-2]
        filname = trainingPath.split(os.path.sep)[-1]
        themeName= filname.split(".")[0]
        if pathName == "plugins":
            themeName= name
        if pathName == "plugins" and filname != "intents.json" :
            continue
        with open(trainingPath, encoding="utf-8") as trainingFile:
            dataTraining= json.load(trainingFile)
            for data in dataTraining:
                subject= themeName+"."+data["subject"]
                sentences = data["sentences"] + data["responses"]
                for sentence in sentences:
                    input.append(bagOfWords(sentence, dictionnary, stopwords))
                    result = [0 for _ in range(len(subjects))]
                    result[subjects.index(subject)]=1
                    outputS.append(result)
                    result2= [0 for _ in range(len(types))]
                    result2[types.index(data["type"])]=1
                    outputT.append(result2)
                    outputV.append(data["value"])
    return input, outputS, outputT, outputV

def getAllIntents(pathName):
    intents=[]
    trainingPaths = list(paths.list_files(pathName, validExts="json"))
    for (i, trainingPath) in enumerate(trainingPaths):
        name = trainingPath.split(os.path.sep)[-2]
        filname = trainingPath.split(os.path.sep)[-1]
        themeName= filname.split(".")[0]
        if pathName == "plugins":
            themeName= name
        if pathName == "plugins" and filname != "intents.json" :
            continue
        with open(trainingPath, encoding="utf-8") as trainingFile:
            dataTraining= json.load(trainingFile)
            for data in dataTraining:
                data["subject"]= themeName+"."+data["subject"]
                intents.append(data)
    return intents

def similitude(sentence1, sentence2, dictionnary, stopwords):
    s1= bagOfWords(sentence1, dictionnary, stopwords)
    s2= bagOfWords(sentence2, dictionnary, stopwords)
    cpt=0
    for i in range(len(s1)):
        if s1[i]==s2[i]:
            cpt+=1
    return cpt/len(s1)

if __name__ == '__main__':
    subjects, types, stopwords, dictionnary = defaultValues()
    print("subjects:", subjects)
    print("types:", types)
    print("stopwords:", stopwords)
    print(dictionnary)
    print(len(dictionnary))