from nltk.tokenize import sent_tokenize, word_tokenize
import re

# Regular Expression dictionary
countAble= '(?:kasus|orang|manusia|korban|jiwa|pasien|meninggal|sembuh|kematian)'
numberFirstFormat = "(?:(?:\d{1,3}\.?)*(?:\d+) %s)" % (countAble)
numberEnum = '(?:satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|puluh|ribu|juta)'
numberSecondFormat = "(?:(?:%s )+%s %s)" % (numberEnum, numberEnum, countAble)
genericNumber = re.compile("(?:%s|%s)" % (numberFirstFormat, numberSecondFormat))

# Construct Format for Date
datenum = '(?:\d{1,2})'
tahun = '(?:\d{4})'
bulan = '(?:januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)'
bulanSingkat = '(?:jan|feb|mar|apr|mei|jun|jul|ags|sep|okt|nov|des)'
day = '(?:senin|selasa|rabu|kamis|jumat|sabtu|minggu)'
dateFirstFormat = "(?:%s, %s (?:%s|%s) %s)" % (day, datenum, bulan, bulanSingkat, tahun)
dateSecondFormat = "(?:\d{1,2}/\d{1,2}/\d{4})"
dateThirdFormat = '(?:kemarin|besok|hari ini|lusa)'

# Construct Format for Time
timeFirstFormat = '(?:\d{2}:\d{2} wib)'
timeSecondFormat = '(?:pukul \d{2}\.\d{2} wib)'
timeThirdFormat = '(?:pagi|siang|sore|malam)'

# Combination of Date and Time
dateTimeFull = "(?:%s,? (?:%s|%s))" % (dateFirstFormat, timeFirstFormat, timeSecondFormat)

# Combine all things into one regular expression
genericDate = "(?:%s|%s|%s)" % (dateFirstFormat, dateSecondFormat, dateThirdFormat)
genericTime = "(?:%s|%s|%s)" % (timeFirstFormat, timeSecondFormat, timeThirdFormat)
genericDateTime = re.compile("(?:%s|%s|%s)" % (dateTimeFull,genericDate, genericTime))


# Return string from a fileName
def ReadText(fileName):
    f = open("../test/"+fileName, "r")
    text = f.read()
    f.close()
    return text

# Extract number format from a sentence
def FindNumber(sentence):
    angka = re.findall(genericNumber, sentence)
    if (len(angka) == 0):
        return "Unknown"
    else:
        return angka[0]

# Extract date from a sentence
def FindDate(sentence):
    tanggal = re.findall(genericDateTime, sentence)
    if (len(tanggal) == 0):
        return "Unknown"
    else:
        return tanggal[0]
      
# Extract article from a text
def ArticleDate(text):
    tanggal = re.findall(genericDateTime, text)
    if (len(tanggal) == 0):
        return "Unknown"
    else:
        return max(tanggal , key = len)