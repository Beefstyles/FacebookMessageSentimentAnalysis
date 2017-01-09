import pandas as pd
import os
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

mainMessageCorpus = pd.read_csv("fullText_Clean.csv",header=0, \
delimiter=",", skip_blank_lines = True)


mainMessageCorpus.dropna(how="all",inplace=False)

mainMessageCorpus = mainMessageCorpus[pd.notnull(mainMessageCorpus["Text Body"])]

#Using the vaderSentiment Analysis
analyzer = SentimentIntensityAnalyzer()

polarityList = []

for body in mainMessageCorpus["Text Body"]:
      if body:
            vs = analyzer.polarity_scores(body)
            polarityList.append(str(vs))
            #print("{:-<65} {}".format(body,str(vs)))
dateList = []
nameList = []
bodyList = []

#Remove empty lines row by row for Date
for date in mainMessageCorpus["Date"]:
      if date:
            dateList.append(date)

#Remove empty lines row by row for Name
for name in mainMessageCorpus["Name"]:
      if name:
            nameList.append(name)

#Remove empty lines row by row for TextBody
for text in mainMessageCorpus["Text Body"]:
      if text:
            bodyList.append(text)

dateDf = pd.DataFrame(dateList,columns=["Date"])
nameDf = pd.DataFrame(nameList,columns=["Name"])
textBodyDf = pd.DataFrame(bodyList,columns=["Text Body"])

splitPolarityList = []
for i in polarityList:
      splitPolarityList.append(i.split(','))


splitDf = pd.DataFrame(splitPolarityList,columns=["Neg","Neu","Pos","Compound"])
splitDf["Neg"] = splitDf["Neg"].str.replace('{\'neg\': ',"")
splitDf["Neu"] = splitDf["Neu"].str.replace('\'neu\': ',"")
splitDf["Pos"] = splitDf["Pos"].str.replace('\'pos\': ',"")
splitDf["Compound"] = splitDf["Compound"].str.replace('\'compound\': ',"")
splitDf["Compound"] = splitDf["Compound"].str.replace('}',"")

non_decimal = re.compile(r'[^\d.]+')


combinedDf = pd.concat([dateDf, nameDf, textBodyDf, splitDf],axis=1)
print (combinedDf.head())


testStr = non_decimal.sub('', 'compound -0.296}')

#polarityDf.to_dict()
#combinedDf.info()

#print (mainMessageCorpus["Text Body"][1])
