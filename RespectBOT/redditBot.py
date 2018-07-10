#PRESS F TO PAY RESPECT, tempo medio senza thread: 50 secondi con il link 6jb6yp
#                        tempo medio Con thread: 20-25 secondi con il link 6jb6yp
#						 nohup python3 /var/www/redditBot.py >& /var/www/tmp &
import sys
import logging
import time
import _thread
import threading
import praw
from praw.models import MoreComments
import sqlite3
from sqlite3 import IntegrityError
from sqlite3worker import Sqlite3Worker
sql_worker = Sqlite3Worker("respect.db")
logging.getLogger("sqlite3worker").setLevel(logging.CRITICAL)


commentiBigArray=[]
lucchetto = False
Master=False
#select count(*) as RespectAmount from rispetto;

def check_updates():    #Metodo che guarda i post e guarda se ci sono almeno 10 commenti nuovi, if so aggiorna 

    query ="SELECT link,commenti,data FROM post"
    reddit = getCredential()
    while(True):
        f=0
        for post in sql_worker.execute(query):  #Apro tutti i link nel db

            #####################
            link= post[0]
            commenti = post[1]               #Prendo i dati di un singolo post
            data = float(post[2])
            #####################
            currentDate=time.time()
            deltaTime = currentDate-data    #Mi calcolo la differenza di tempo tra adesso e la creazione del post    
            #####################
            if(deltaTime<345600):  #Se la differenza è minore di 5 giorni: 
                submission = reddit.submission(link)
                print("Checking already written post: "+submission.fullname)
                n_commenti = submission.num_comments
                try:
                    getId = "SELECT id FROM post where link='"+link+"';";   #Mi prendo l'id del post dato il link
                    currentId=0;
                    for ida in sql_worker.execute(getId):
                        currentId=ida[0];
                    q = "UPDATE post SET Commenti="+str(n_commenti)+" WHERE id="+str(currentId) #aggiorno il numero di commenti 
                    sql_worker.execute(q)
                except (AttributeError,IntegrityError) as error:print("error")

                getId = "SELECT id FROM post where link='"+link+"';"; #Mi prendo l'id del post dato il link
                currentId=0;
                for ida in sql_worker.execute(getId):
                    currentId=ida[0];
                res = getAll(submission,n_commenti)
                f=0
                for x in range(0, len(res)):
                   elem = res[x]
                   if hasattr(elem, 'body'):
                       try:
                           testo= str(res[x].body)
                           autore = str(res[x].author)
                           if(testo=='f' or testo=='F'):
                              f=f+1
                              domanda = "INSERT INTO rispetto(user,post) VALUES('"+autore+"','"+str(currentId)+"')"   #Scrivo su rispetto 
                              sql_worker.execute(domanda)
                       except (IntegrityError) as error: print("error")
                         


    return True

def getSubComments(comment, verbose=True):
  global lucchetto
  global commentiBigArray
  if(Master):
      #_Thread_stop()
      print("Morto")
  if(lucchetto==False):
      lucchetto=True
      commentiBigArray.append(comment)
      lucchetto=False
      if not hasattr(comment, "replies"):
        replies = comment.comments()
        lucchetto=True
        if verbose: print("fetching (" + str(len(commentiBigArray)) + " comments fetched total)")
        lucchetto=False
      else:
        replies = comment.replies
      for child in replies:
         getSubComments(child, verbose=verbose)
  else: 
      time.sleep(0.05)
def getAll(submission,n, verbose=True):
  global commentiBigArray
  commentiBigArray=[]
  print("Scaricando Commenti ....")
  comments = submission.comments
  index = 0
  for comment in comments:
    time.sleep(0.08)
    _thread.start_new_thread(getSubComments, (comment,verbose))
  
  temp0 = 0
  temp1 = len(commentiBigArray)

  while(temp1>temp0):
      time.sleep(2)
      temp0=temp1
      temp1= len(commentiBigArray)
  Master=True
  return commentiBigArray
def getCredential(): 
    return praw.Reddit(client_id='YOUR-ID',
                     client_secret='YOUR-SECRET',
                     password='PASS',
                     user_agent='testscript by /u/BOT',
                     username='USERNAME')
def principale(subred):   #Metodo che cerca i post nuovi su /r/dankmemes e /r/me_irl
    print("Service Started");
    reddit = getCredential()
    print(reddit.user.me())
    while True:
        for submission in reddit.subreddit(subred).new(limit=25): #Guardo i primi 25 commenti (new), piglio link,ncommenti e date e li metto nel database.
            print("Aggiungendo post")
            link= submission.id 
            submission = reddit.submission(link)
            n_commenti = submission.num_comments
            data = submission.created
            querypost = "INSERT INTO post(link,Commenti,data,subreddit) VALUES('"+submission.permalink+"','"+str(n_commenti)+"','"+str(data)+"','"+subred+"')"
            sql_worker.execute(querypost)


_thread.start_new_thread(check_updates,())
a="dankmemes"
b="Me_irl"
_thread.start_new_thread(principale,(a,))
_thread.start_new_thread(principale,(b,))
while(True): time.sleep(1000)