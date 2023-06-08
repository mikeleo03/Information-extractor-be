import re

# Looking for pattern on text using regex
def RegexPatternMatching(text, pattern):
    found = re.search(pattern, text)
    return found

# Return sentence which contains pattern
def GetPatternRegex(sentence, pattern):
    sentencePattern = []
    for i in range(len(sentence)):
        if (RegexPatternMatching(sentence[i], pattern)):
            sentencePattern.append(sentence[i])
    return sentencePattern