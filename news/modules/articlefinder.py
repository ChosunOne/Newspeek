from newspaper import Article

def getArticleText(articleurl):
    article = Article(articleurl)
    article.download()
    article.parse()

    return article.text