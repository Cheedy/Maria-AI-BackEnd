import tools
import random

class PluginDefault:

    def __init__(self, subject, typeS):
        self.intents = tools.getAllIntents("plugins")
        self.intents += tools.getAllIntents("training_data")
        self.subject= subject
        self.typeS= typeS
    
    def intentsBySubject(self, name):
        intents=[]
        for i in range(len(self.intents)):
            if self.intents[i]["subject"].split(".")[0]==name:
                intents.append(self.intents[i])
        return intents

    def searchSentence(self, sentence, subject, intents):
        subjects, types, stopwords, dictionnary = tools.defaultValues()
        best=-1
        bestIndex=-1
        for i in range(len(intents)):
            if intents[i]["subject"]==subject:
                for j in range(len(intents[i]["sentences"])):
                    tmp=  tools.similitude(sentence, intents[i]["sentences"][j], dictionnary, stopwords)
                    if best < tmp:
                        best= tmp
                        bestIndex=j
                if len(intents[i]["sentences"]) > bestIndex + 1:
                    return intents[i]["sentences"][bestIndex]+"\n"+intents[i]["sentences"][bestIndex+1]
                elif bestIndex - 1 > 0:
                    return intents[i]["sentences"][bestIndex-1]+"\n"+intents[i]["sentences"][bestIndex]
                else:
                    return intents[i]["sentences"][bestIndex]
        return "Pas mal la punchline"

    def response(self, sentence=""):
        #HUMOR
        if self.subject=="humor.joke":
            intents= self.intentsBySubject("humor")
            joke= intents[random.randrange(len(intents))]
            if(joke["subject"]=="humor.joke"):
                return "Toi "+ joke["sentences"][0]
            return joke["sentences"][0]

        #RAP
        if self.subject.split(".")[0]=="rap":
            intents= self.intentsBySubject("rap")
            return self.searchSentence(sentence, self.subject, intents)

        #DEFAULT
        for i in range(len(self.intents)):
            if self.intents[i]["subject"]==self.subject and self.intents[i]["type"]==self.typeS:
                return self.intents[i]["responses"][random.randrange(len(self.intents[i]["responses"]))]
        return "Je n'ai pas de réponse"
