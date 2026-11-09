from bs4 import BeautifulSoup
from urllib.request import urlopen
from email.message import EmailMessage
import smtplib
import os
import json

from cryptography.fernet import Fernet
from dotenv import load_dotenv


sendEmail = ""
sendPassword = ""
receiveEmail = ""

votd = "https://www.bible.com/verse-of-the-day"
Bible = {}

url = ""
urls = ["https://hacker-news.firebaseio.com/v0/topstories.json","https://thehackernews.com/"]

thnArticles = {}
HNArcticles = {}

myTopics = ["Flaw","Flaws","Malware","Backdoor","Backdoors","exploit","ransomeware", "hack", "hacking"]

def get_credemtials():
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    assert SECRET_KEY
    FERNET = Fernet(SECRET_KEY)
    global sendEmail
    global sendPassword
    global receiveEmail

    with open('Credentials.txt') as f:
        for x,line in enumerate(f):
            match x:
                case 0:
                    sendEmail = FERNET.decrypt(line).decode()
                case 1:
                    sendPassword = FERNET.decrypt(line).decode()
                case 2:
                    receiveEmail = FERNET.decrypt(line).decode()

#soupEdit = (soup.get_text().strip("\r\t"))
def get_votd(soup):
    words = soup.find('a',class_="w-full text-primary no-underline")
    verse = soup.find('a',class_="w-full no-underline")
    Bible["text"] = words.text.strip()
    Bible["verse"] = verse.text.strip()


def organizeTHN(soup):
    articleTitles = soup.find_all(["h2"])
    articleStoryLink = soup.find_all('a', class_="story-link")
    articleSummary = soup.find_all('div', class_="home-desc")
    articleDiv = soup.find_all('a', class_="pop-link")
    for x,title in enumerate(articleTitles):
        for topic in myTopics:
            if topic.lower() in title.text.strip().lower():
                titlesummary = articleSummary[x].text.strip()
                titlelink = articleStoryLink[x].get('href')
                thnArticles[f'Title{x}'] = {"summary":titlesummary, "link":titlelink}
            else:
                pass
def organizeHN(soup):
    numbersHold = ""
    for number in soup:
        numbersHold = number
    numbersList = numbersHold.split(',')
    for x,i in  enumerate(numbersList):
        if "[" in i:
            numbersList[x] = i.strip("[")
        elif "]" in i:
            numbersList[x] = i.strip("]")
    for number in numbersList:
        url = "https://hacker-news.firebaseio.com/v0/item/" + number + ".json"
        print(url)
        page = urlopen(url)
        htmlBytes = page.read()
        html = htmlBytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        try:
            jsonData = json.loads(soup.get_text())
            for topic in myTopics:
                if topic.lower() in jsonData["title"].lower():
                    HNArcticles[jsonData["title"]] = jsonData["url"]
        except json.decoder.JSONDecodeError as e:
            pass

def openPage(url):
    page = urlopen(url)
    htmlBytes = page.read()
    html = htmlBytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(url)
    if "bible" in url:
        get_votd(soup)
    elif "hackernews" in url:
        organizeTHN(soup)
    elif "hacker-news" in url:
        organizeHN(soup)
    else:
        print('Website not set up for scraping and readibility in program yet')

def send_email():
    print("Sending message")
    msg = EmailMessage()
    msg['to'] = receiveEmail
    msg['from'] = sendEmail
    msg['subject'] = "Python Automated News Email"
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(sendEmail,sendPassword)
    message = f"""\
    <html>
        <body>
            <p>{Bible["verse"]}<br>
                {Bible["text"]}<br>
            </p>
        </body>
    </html>
"""
    thnmessage = "TheHackerNews: \n"
    for x,article in enumerate(thnArticles):
        title = f"Title{x}"
        try:
            thnArticles[title]
            thnmessage = thnmessage + thnArticles[title]["summary"] + thnArticles[title]["link"] + "\n"
        except KeyError:
            pass
    message += thnmessage + "\n HACKERNEWS \n" + str(HNArcticles)
    msg.add_alternative(message,subtype='html')
    s.send_message(msg)
    s.quit()

if __name__ == "__main__":
    get_credemtials()
    openPage(votd)
    if url:
        openPage(url)
    elif urls:
        for url in urls:
            openPage(url)
    else:
        print("No URL or URLS")
    send_email()
    print("Email sent")

