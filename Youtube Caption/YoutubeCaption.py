import urllib.request
import json
import sqlite3
from bs4 import BeautifulSoup


PlayListURL = "UU-lHJZR3Gqxm24_Vd_AJ5Yw"
ChannelName = "PewDiePie"
url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&key=AIzaSyBF89Cf4JoRnLKnC9yWBsA_NsNFPpocnP8&playlistId="+PlayListURL
conn = sqlite3.connect('Youtube.db')
cursorWrite = conn.cursor()
divisore=80;
def WriteVideo(video):
    leng= len(video)
    for i in range(leng):
        videos = video[i]
        snippet = videos["snippet"]
        title = ""+snippet["title"]
        data = snippet["publishedAt"]
        author = snippet["channelTitle"]
        link = snippet["resourceId"]["videoId"]
        title=title.replace('\'','');
        query = "INSERT INTO Video(Titolo,Link,Tag) VALUES (" + ascii(title) + ", '" + link + "','" + author + "') ;";
        'print(query)'
        c = conn.cursor()
        c.execute(query)
    conn.commit();


def GetPlaylist():
   urlMod = url+""
   try:
       while True:
            risposta = json.loads(urllib.request.urlopen(urlMod).read().decode("utf8"))
            videos = risposta["items"]
        
            WriteVideo(videos);
            Token = risposta["nextPageToken"]
            page = risposta["pageInfo"]["totalResults"];
            if(page>50):
                tot = risposta["pageInfo"]["totalResults"]
                urlMod = url + "&pageToken=" + Token
                x = 0
            print(urlMod)
   except Exception:
        print("Errore")

def ScriviFrasi():
    cont = 1
    query =  "Select link from Video where Tag='"+ChannelName+"'"
    c = conn.cursor()
    ex = c.execute(query)
    nVideo=0
    for row in ex:
        nVideo+=1 
    ex = c.execute(query)
    global divisore
    while(nVideo%divisore!=0):
        divisore-=1

    for row in ex:
        apiURL = "https://www.youtube.com/api/timedtext?v="+row[0]+"&lang=en";
        try:
            html = urllib.request.urlopen(apiURL).read().decode("utf8");    
        except Exception:
            print("Errore")
        if(html==''):  #Se i sottotitoli sono nuovi e non funziona questa semplice api devo caricare il link del video e pigliarli da lì
            videoUrl= "https://www.youtube.com/watch?v="+row[0]
            html = urllib.request.urlopen(videoUrl).read().decode("utf8");
            soup = BeautifulSoup(html, 'html.parser')
            bool = True
            startUrl=0
            endUrl=0
            scr =  soup.find_all("script")
            for script in scr:
                sc = script.next
                count=0
                if(sc.startswith("var ytplayer")):
                    while(bool):
                        count=count+1
                        startUrl = sc.find("https:\/\/www.youtube.com\/api\/tim",startUrl+1);
                        if (startUrl > -1):     #se Trovo la scritta qua sopra
                            endUrl = sc.find("\"name",endUrl+1) #Modifico l'url fatto bene per fare la richiesta http
                            myURL = sc[startUrl:endUrl-4]
                            myURL= myURL.replace("u0026", "&")      
                            myURL= myURL.replace("\\", "")
                            l = len(myURL)
                            if(myURL[l-2:l]=='en'): #se lo trovo in inglese devo guardare se ci sono solo i sottotitoli generati automaticamente, oppure altre cose 
                               bool=False
                               if(count>1): #Se sono generati automaticamente non ci entra neanche, altrimenti cerco quello in uk (en-GB)
                                   myURL= myURL.replace("&kind=asr","")
                                   myURL= myURL.replace("lang=en","lang=en-GB")
                            html= urllib.request.urlopen(myURL).read().decode("utf8")   
                        
                        else:
                            bool=False
            print("Processed: +1, "+str(cont))
        else: print("Normal: +1, "+str(cont))
        cont=cont+1
        try:
            html=html.encode('utf8')
            ScriviVideo(html,row[0],cont)
        except Exception:
            print("Errore")



       
def ScriviVideo(xml,link,cont): #Dato un xml di sottotitoli, Scrive nel database i sottotitoli
    soup = BeautifulSoup(xml, 'html.parser')
    getId = "SELECT ID FROM Video where link='"+link+"';";
    id=0
    for ida in cursorWrite.execute(getId):
        id=ida
    for text in soup.find_all("text"):
        testo  = text.next
        start = text.get("start")
        dur = text.get("dur")
        testo = testo.replace("<font color=\"#E5E5E5\">","").replace("<font color=\"#CCCCCC\">","").replace("</font>","")
        start =""+start
        dur = ""+dur
        query = "INSERT INTO Frase(FK_Video,testo,inizio,durata) VALUES('" + str(id[0]) + "','" + testo + "','" + ""+start + "','" + ""+dur + "')";
        cursorWrite.execute(query)
        global divisore
        if(cont%divisore==0):
            conn.commit();
        