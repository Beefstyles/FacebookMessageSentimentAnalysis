import pandas as pd
import os
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.style.use('ggplot')

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

nameFreqCount = combinedDf['Name'].value_counts().to_dict()
nameFreqDf = pd.DataFrame(list(nameFreqCount.items()),columns=['Name','Frequency'])

plt.pie(
      nameFreqDf['Frequency'],
      labels=nameFreqDf['Name'],
      shadow=False,
      colors=None, 
)

plt.axis('equal')

plt.tight_layout()
plt.show(block = True)
