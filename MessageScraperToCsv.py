import csv
import re
from bs4 import BeautifulSoup

html_file = "messages.htm"
page = open(html_file, encoding='UTF-8')

soup = BeautifulSoup(page,'html.parser')

metaData = soup.find_all('span',attrs={'class':'meta'})
userData = soup.find_all('span',attrs={'class':'user'})

postData = soup.find_all('p')


data = []

data.append((metaData, userData, postData))

print("Write Date csv")
with open('dateText.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file,dialect='excel', delimiter=',')
    writer.writerow(["Date"])
    for dates, names, body in data:
        for dateText in dates:
            writer.writerow([dateText.get_text()])
    csv_file.close()

print("Write Names csv")
with open('namesText.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file,dialect='excel', delimiter=',')
    writer.writerow(["Name"])
    for dates, names, body in data:
        for nameText in names:
            writer.writerow([nameText.get_text()])
    csv_file.close()

print("Write Body Text csv")
with open('bodyText.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file,dialect='excel', delimiter=',')
    writer.writerow(["Text Body"])
    for dates, names, body in data:
        try:
            for bodyText in body:
                bodyTextToPrint = bodyText.get_text()
                if bodyTextToPrint is not None:
                    writer.writerow([bodyTextToPrint])                       
        except Exception as e:
            print(e)
            continue
    csv_file.close()
    
print("Done!")