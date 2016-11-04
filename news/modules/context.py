import textblob
import os
from nltk.tag.stanford import StanfordNERTagger 
from collections import Counter

java_path = "C:/Program Files (x86)/Java/jre1.8.0_111/bin/java.exe"
os.environ['JAVAHOME'] = java_path

class Context:
    def __init__(self, articleText):
        self.blob = textblob.TextBlob(articleText)
        #blob.tags
        keywords = [x[0] for x in self.blob.tags if "NNP" in x[1] or "NN" in x[1] or "CD" in x[1]]
        self.keywords = set(keywords)
        self.nounPhrases = Counter(self.blob.noun_phrases).most_common()
        st = StanfordNERTagger('D:/Source/Newspeek/Newspeek/news/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz', 
            'D:/Source/Newspeek/Newspeek/news/stanford-ner-2014-06-16/stanford-corenlp-caseless-2015-04-20-models.jar')
        self.namedEntities = dict((a.lower(), b) for a, b in set([x for x in st.tag(articleText.split()) if x[1] != 'O']))
        self.namedPhrases = {}

        for np in self.nounPhrases:
            tags = []
            for word in np[0].split():
                tag = 'O'
                if word.lower() in self.namedEntities.keys():
                    tag = self.namedEntities[word.lower()]
                tags.append(tag)

            np_tag = Counter(tags).most_common(1)[0][0]
            if np_tag != 'O':
                self.namedPhrases[np[0].lower()] = np_tag
            
        pass

