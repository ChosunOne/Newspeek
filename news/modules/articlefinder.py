from newspaper import Article
from textblob import TextBlob
import os
import google
import requests


class ArticleFinder: 
    def __init__(self, initialURL, followUpQuery):
        self.initialURL = initialURL
        self.prevQuery = None
        self.query = followUpQuery

        article = Article(self.initialURL)
        article.download()
        article.parse()

        blob = TextBlob(article.text)
        keywords = [x[0] for x in blob.tags if "NNP" in x[1] or "NN" in x[1] or "CD" in x[1]]
        nounPhrases = blob.noun_phrases
        uniqueNP = []
        [uniqueNP.append(item) for item in nounPhrases if item not in uniqueNP]
        wordfrequencies = []

        for keyword in uniqueNP:
            wordfrequencies.append(blob.words.count(keyword))

        listofindices = sorted(range(len(wordfrequencies)), key=lambda ix: wordfrequencies[ix])
        
        searchword1Index = listofindices[-1]
        searchword2Index = listofindices[-2]

        searchword1 = uniqueNP[searchword1Index]
        searchword2 = uniqueNP[searchword2Index]

        #Search Google for Query 

        question = self.query

        auxiliaryVerbs = ['do', 'will', 'did', 'Do', 'Will', 'Did']
        questionWords = ['who', 'what', 'when', 'where', 'why', 'Who', 'What', 'When', 'Where', 'Why', 'Will', 'will']
        toBeVerbs = ['Am', 'Are', 'Was', 'Were', 'am', 'are', 'was', 'were']

        question = question.split()

        questionWord = None
        auxiliaryVerb = None
        toBeVerb = None
        subject = None
        mainVerb = None

        if len(question) >= 5: 
            if question[0] in auxiliaryVerbs: 
                if question[1] == "else":
                    auxiliaryVerb = question[0]
                    subject = question[1]
                    mainVerb = question[2]
                    modulator = question[3:]

                    question[1] = searchword1

                    question.append("-" + searchword2)

                else:
                    auxiliaryVerb = question[0]
                    subject = question[1]
                    mainVerb = question[2]
                    modulator = question[3:]

                    question[1] = searchword1

                self.query = " ".join(question)
                

            if question[0] in questionWords and question[1] in auxiliaryVerbs:
                questionWord = question[0]
                auxiliaryVerb = question[1]
                subject = question[2]
                mainVerb = question[3]
                modulator = question[4:]

                question[2] = searchword1
                

                self.query = " ".join(question)
                


            if question[0] in toBeVerbs:
                mainVerb = question[0]
                subject = question[1]
                modulator = question[2:]

                question[1] = searchword1

                self.query = " ".join(question)
                

            if question[0] in questionWords and question[1] in toBeVerbs:
                questionWord = question[0]
                toBeVerb  = question[1]
                subject = question[2]
                modulator = question[3:]

                question[2] = searchword1

                self.query = " ".join(question)
                

            else: 
                question.append(searchword1)
            #    question.append(searchword2)
                self.query = " ".join(question)
                
        if len(question) == 4: 
            if question[0] in auxiliaryVerbs: 
                if question[1] == "else":
                    auxiliaryVerb = question[0]
                    subject = question[1]
                    modulator = question[2:]

                    question[1] = searchword1

                    question.append("-" + searchword2)

                else:
                    auxiliaryVerb = question[0]
                    subject = question[1]
                    modulator = question[2:]

                    question[1] = searchword1

                self.query = " ".join(question)
                


            if question[0] in toBeVerbs:
                mainVerb = question[0]
                subject = question[1]
                modulator = question[2:]

                question[1] = searchword1

                self.query =  " ".join(question)
                


            if question[0] in questionWords and question[1] in toBeVerbs:
                questionWord = question[0]
                toBeVerb  = question[1]
                subject = question[2]
                modulator = question[3:]

                question[2] = searchword1

                self.query = " ".join(question)
                
            else:
                question.append(searchword1)
            #    question.append(searchword2)
                self.query = " ".join(question)
                    

        if ((len(question) >= 0) and (len(question) < 4)): 
            question.append(searchword1)
            question.append(searchword2)
            self.query = " ".join(question)
            

        response = google.search(self.query, tld='com', lang='en', num=5, start=0, stop=5)

        resultArray = []
        for result in response: 
            resultArray.append(str(result))

        responseArticle = Article(resultArray[0])
        responseArticle.download()
        responseArticle.parse()

        self.responseArticleText = responseArticle.text
        self.finalURL = resultArray[0]

