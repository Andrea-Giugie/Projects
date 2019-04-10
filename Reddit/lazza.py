import praw
import requests
import pymysql
import time

url = "https://pay.reddit.com/user/obscurewinter/comments.json?t=all&limit=5"

connection = pymysql.connect(host='localhost',
                             user='user',
                             password='password',
                             db='Reddit',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor(pymysql.cursors.DictCursor)

reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     username='CiManchi_Bot',
                     password='password',
                     user_agent='user_agent')
while(True):
    try:
        r = requests.get(url, headers={'User-agent': 'v0.1'})
        a = r.json()["data"]["children"]
        for children in a:
            commentoText = children["data"]["body"]
            print(commentoText)
            id = children["data"]["id"]
            permalink = children["data"]["permalink"]

            sql = "SELECT * FROM Commenti WHERE idCommento ='%s'"
            cur.execute(sql % id)
            entrato = False
            for row in cur:
                entrato = True

            if(entrato):

                print("Salto il commento con id: "+str(id)+" ")
            else:
                try:
                    commento = reddit.comment(id)
                    commento.reply("Ci manchi")
                    reddit.redditor('MyUser').message(
                        'Ho Scritto a lazza', 'Dai un occhiata a questo link: '+str(permalink))
                    time.sleep(5)
                    print("Ho scritto il commento ")

                    with connection.cursor() as cursor:
                        sql = "INSERT INTO Commenti (Commento,idCommento) VALUES (%s, %s)"
                        cursor.execute(sql, (commentoText, id))

                    connection.commit()
                except Exception as e:
                    print(e)
                print("errore")
        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(300)
