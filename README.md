################################################
# Programmeerimine I
# 2024/2025 sügissemester
# Projekt

<br>

# Teema: USA kahe poliitiliselt vastanduva meediaväljaande pealkirjade analüüs enne USA presidendi valimisi. 

### Autorid: Karl-Christofer Veske ja Karita-Liis Grassmanni

## Kirjeldus ja käivitus:
Lahendus koosneb mitmest eraldi Pythoni scriptist, mis kas koguvad või analüüsivad teksti ja väljutavad .csv-sid. Ja Jupyteri notebookist, kus toimub analüüs ning andmete visualiseerimine. 

Pealkirjad kogutakse vasakpoolselt populaarseimalt väljaandest CNN ja parempoolsest, CNNile vastanduvast Fox Newsist. Andmed on kogutud 27.10.2024. 


<br>

Pythoni skriptid ja nende kirjeldused:

<br>

<b>CNN_Scraper - : </b> vastav koodijupp <i> scrapeib </i> CNNi veebilehte ning väljutab .csv, kus on üks tulp: headlines. Seal on uudiste pealkirjad. 

<b> foxnews_scraper - </b> vastav koodijupp <i> scrapeib </i> Fox Newsi veebilehte ning väljutab .csv, kus on üks tulp: headline. Seal on uudiste pealkirjad.  

<b>CNN_Sentiment & fox_news_sentiment - </b> vastav koodijupp analüüsib .csv-st imporditavaid pealkirju ning kasutades nltk moodulit, teeb tekstile sentiment analüüsi. (Paneb -1:1 skaalale, kui positiivne/negatiivne tekst on). Tulemus väljutatakse .csv-na. 

<b> clickbait_analyzer - </b> vastav koodjupp analüüsib .csv-s olevaid pealkirju ning paneb paika kui "clickbaity" vastav pealkiri on. Ta vaatab kindlate nö "trigger"sõnade osakaalu pealkirjades. 

<b> create_wordcloud - </b> vastav koodjupp analüüsib sõnade esinevust pealkirjades ning loeb kokku, kui mitu korda esines nt sõna Trump CNN-i pealkirjades. 

<b> grade_analyzer - </b> Vastav koodijupp analüüsib, mitmenda kooliklassi tasemele pealkirjad vastavad. See tugineb Flesch-Kincaidi meetodidele ning see meetod on ka sisse ehitatud textstat moodulisse, mida me antud juhul kasutame

<b> Vajalikud lisad</b>
<br>
Jupyter Notebook

Moodulid: BeautifulSoup, pandas, seaborn, matplotlib, nltk, Wordcloud, Counter, textstat re, os, TextBlob

Töö valmistamisel on kasutaud ka Claude(3.5 Sonnet) ja ChatGPT(GPT-4o mini) juturoboteid. 
##################################################
