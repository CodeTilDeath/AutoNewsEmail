# News Scraping Automation Tool

A Python-based automation bot that scrapes two key sources of information and a daily bible verse:
- **Verse of the Day** from Bible.com
- **Hacker News Top Stories** from news.ycombinator
- **The Hacker News main page** from thehackernews

It organizes these items based on predefined keywords and sends an email summary to the user via SMTP.

---

## 📋 Features

- Scrapes daily Bible verse and relevant articles from Hacker News and The Hacker News
- Extracts specific topics inputted by users in code (Malware, Exploit, etc.) from article titles
- Sends automated emails with content summaries to a designated recipient
- Uses encrypted credentials stored securely

---

## 🔧 Installation Requirements

1. Python 3.x installed
2. Required packages: `BeautifulSoup`, `urllib.request`, `email.message`, `smtplib`, `cryptography`, `python-dotenv`

Install dependencies:
```bash
pip install beautifulsoup4 urllib3 cryptography python-dotenv
