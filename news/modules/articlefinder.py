from newspaper import Article
from textblob import TextBlob
import os
import google
import requests


looping = True
initialURL = None
prevQuery = None
question1 = None

#Get text of initial article
while(looping):
	if initialURL is None:
		initialURL = raw_input('Hello! Please enter the URL you would like to chat about: ')

	article = Article(initialURL)
	article.download()
	article.parse()

	print article.text

	#Do NLP

	blob = TextBlob(article.text)
	keywords = [x[0] for x in blob.tags if "NNP" in x[1] or "NN" in x[1] or "CD" in x[1]]
	nounPhrases = blob.noun_phrases
	wordfrequencies = []

	for keyword in nounPhrases:
		wordfrequencies.append(blob.words.count(keyword))

	listofindices = sorted(xrange(len(wordfrequencies)), key=lambda ix: wordfrequencies[ix])
	
	searchword1Index = listofindices[-1]
	searchword2Index = listofindices[-2]

	searchword1 = nounPhrases[searchword1Index]
	searchword2 = nounPhrases[searchword2Index]

	#Search Google for Query 

	question = raw_input ('Follow-up Query: ')
	
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
			auxiliaryVerb = question[0]
			subject = question[1]
			mainVerb = question[2]
			modulator = question[3:]

			question[1] = searchword1

			question1 = " ".join(question)
			prevQuery = question1

		elif question[0] in questionWords and question[1] in auxiliaryVerbs:
			questionWord = question[0]
			auxiliaryVerb = question[1]
			subject = question[2]
			mainVerb = question[3]
			modulator = question[4:]

			question[2] = searchword1
			

			question1 = " ".join(question)
			prevQuery = question1


		elif question[0] in toBeVerbs:
			mainVerb = question[0]
			subject = question[1]
			modulator = question[2:]

			question[1] = searchword1

			question1 = " ".join(question)
			prevQuery = question1

		elif question[0] in questionWords and question[1] in toBeVerbs:
			questionWord = question[0]
			toBeVerb  = question[1]
			subject = question[2]
			modulator = question[3:]

			question[2] = searchword1

			question1 = " ".join(question)
			prevQuery = question1


	elif len(question) == 4: 

		if question[0] in auxiliaryVerbs: 
			auxiliaryVerb = question[0]
			subject = question[1]
			mainVerb = question[2]
			modulator = question[3:]

			question[1] = searchword1

			question1 =  " ".join(question)
			prevQuery = question1


		elif question[0] in toBeVerbs:
			mainVerb = question[0]
			subject = question[1]
			modulator = question[2:]

			question[1] = searchword1

			question1 =  " ".join(question)
			prevQuery = question1


		elif question[0] in questionWords and question[1] in toBeVerbs:
			questionWord = question[0]
			toBeVerb  = question[1]
			subject = question[2]
			modulator = question[3:]

			question[2] = searchword1

			question1 = " ".join(question)
			prevQuery = question1

			
	else: 

		question1 = prevQuery

	print question1

	response = google.search(question1, tld='com', lang='en', num=5, start=0, stop=5)

	resultArray = []
	for result in response: 
		resultArray.append(str(result))

	responseArticle = Article(resultArray[0])
	responseArticle.download()
	responseArticle.parse()

	print responseArticle.text


	done = raw_input('Done chatting?')
	if done == "yes" or done == "Yes":
		looping = False
	else: 
		looping = True


