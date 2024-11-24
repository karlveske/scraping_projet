################################################
# Programmeerimine I
# 2024/2025 sügissemester
# Projekt

<br>

# Teema: USA kahe poliitiliselt vastanduva meediaväljaande pealkirjade analüüs enne presidendi valimisi. 

# Autorid: Karl-Christofer Veske ja Karita-Liis Grassmanni

# Kirjeldus ja käivitus:
Lahendus koosneb mitmest eraldi Pythoni scriptist, mis kas koguvad või analüüsivad teksti ja väljutavad .csv-sid. Andmeanalüüs ja visualiseerimine toimub Jupyteri notebookis. 

<br>



Pythoni skriptid ja nende kirjeldused:
<br>
<b>CNN_Scraper: </b> vastav koodijupp <i> scrapeib </i> CNNi veebilehte ning väljutab .csv, kus on üks tulp: headlines. Seal on kõigi saidi pealkirjad. 

<b> foxnews_scraper </b> vastav koodijupp <i> scrapeib </i> Fox Newsi veebilehte ning väljutab .csv, kus on üks tulp: headline. Seal on kõigi saidi pealkirjad.  

<b>CNN_Sentiment ja fox_news_sentiment</b> vastav koodijupp analüüsib .csv-st imporditavaid pealkirju ning kasutades nltk moodulit, teeb tekstile sentiment analüüsi. (Paneb -1:1 skaalale, kui positiivne/negatiivne tekst on)

<b> clickbait_analyzer</b>

<b> create_wordcloud </b>

<b> grade_analyzer </b>

<b> Vajalikud lisad</b>
<br>
Jupyter Notebook

Moodulid: BeautifulSoup, pandas, seaborn, matplotlib, nltk, Wordcloud, Counter, re, os

Töö valmistamisel on kasutaud ka Claude(3.5 Sonnet) ja ChatGPT(GPT-4o mini) juturoboteid. 
##################################################
