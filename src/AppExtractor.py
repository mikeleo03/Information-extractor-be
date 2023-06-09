# Modul Import
from src.BMPattern import *
from src.KMPPaterrn import *
from src.RegexPattern import *
from src.DataExtractor import *
import re

# Highlighting matched words
def BoldMatches(sentence, matches):
    return sentence.replace(matches, "<b>"+matches+"</b>")

# Underlining matched words
def UnderlineMatches(sentence, matches):
    return sentence.replace(matches, "<u>"+matches+"</u>")

# Extraction process from file input
def BeginExtraction(keyword, method, file, text):
    # Main
    extractedSentence = []  
    sentence = []           
    sentencePattern = [] 
    
    text = text.lower()
    articleDate = ArticleDate(text)
    sentence = sent_tokenize(text)

    # Pattern Matching
    if (method == "BM"):
        sentencePattern = GetPatternBMSentence(sentence, keyword)
    elif (method == "KMP"):
        sentencePattern = GetPatternKMPSentence(sentence, keyword)
    elif (method == "Regex"):
        sentencePattern = GetPatternRegex(sentence, keyword)

    # If there is no pattern which contains keyword
    if ((len(sentencePattern) == 0)):
        return (file, text, extractedSentence, 0)

    # If found
    else:
        # Extraction Data
        for j in range(len(sentencePattern)):
            jumlah = FindNumber(sentencePattern[j])
            tanggal = FindDate(sentencePattern[j])
            if not(jumlah == "Unknown"):
                sentencePattern[j] = UnderlineMatches(sentencePattern[j], jumlah)
            if not(tanggal == "Unknown"):
                sentencePattern[j] = UnderlineMatches(sentencePattern[j], tanggal)
            else:
                tanggal = articleDate
                
            # Highlight only if it is not a trailing space
            if (not re.match(r'^\s*$', keyword)):
                sentencePattern[j] = BoldMatches(sentencePattern[j], keyword)
            extractedSentence.append((sentencePattern[j].capitalize(), jumlah, tanggal.capitalize()))

        return (file, text, extractedSentence, len(sentencePattern))