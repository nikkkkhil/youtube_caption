#!/usr/bin/env python
# coding: utf-8



import re
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import argparse
import subprocess
import mysql.connector
import requests
from bs4 import BeautifulSoup


class my_dictionary():
    def __init__(self):
        self.mydb = mysql.connector.connect(host = 'localhost',user='root',passwd ='rock',database='dictionary')
        self.mycursor = self.mydb.cursor(buffered=True)
        self.links = []
    def check_video(self,url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        elements = soup.find_all("h3")
        for el in elements:
            if len(el('a')) ==0:
                continue
            else:
                dlink = "https://www.youtube.com"+el('a')[0]["href"]
                return(dlink)
            
    def capt_download(self,link):
        self.link = link
        bashCommand = "./ytcap.sh %s"%self.link
        print(bashCommand)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    
    def caption_extract(self):    
        txt = " "
        with open('/home/nikhil/Desktop/youtube_CC/caption.en.vtt') as f:
            lines = f.readlines()
        f.close()
        for check in lines:
            txt += check
        stop_words = set(stopwords.words('english')) 
        txt = txt.lower()
        result = re.sub(r'\d+','', txt)
        result = result.replace("<c>"," ")
        result = result.replace("</c>"," ")
        translator = result.maketrans('', '', string.punctuation)
        data = result.translate(translator)
    
        word_tokens = word_tokenize(data) 
    
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    
        filtered_sentence = [] 
    
        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w) 
        filtered_sentence = list(set(filtered_sentence))
        return(filtered_sentence)

    
    def inser_value(self,table,column,value):
        self.table = table 
        self.column = (column) 
        self.value = value 
        mySql_insert_query = """INSERT INTO """+self.table+" "+"("+self.column+")"+""" VALUES ('%s') """%self.value
        print(mySql_insert_query)
        self.mycursor.execute(mySql_insert_query)
        self.mydb.commit()
    
    def check_db(self,table,column,value):
        self.table = table 
        self.column = column  
        self.value = value 
        self.mycursor.execute("SELECT * FROM "+self.table+" WHERE "+self.column+ " = %s",(self.value,))
        row_count = self.mycursor.rowcount
    #     print ("number of affected rows: {}".format(row_count))
        if row_count == 0:
    #         print ("%s It Does Not Exist"%value)
            return False
        else:
            return True 

    def telegram_bot_sendtext(self,bot_token,bot_chatID,bot_message):
        self.bot_token =  bot_token
        self.bot_chatID = bot_chatID
        self.bot_message = bot_message
        self.send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chatID + '&parse_mode=Markdown&text=' + self.bot_message
    
        response = requests.get(self.send_text)
    
        return response.json()
    def new_word(self,word):
        self.word = word
        print(self.word)
        self.telegram_bot_sendtext(<your telegram api>,<your telegram channel id>,'%s'%self.word)
    

# mycursor.execute("CREATE TABLE dictionary (id INT AUTO_INCREMENT PRIMARY KEY, words VARCHAR(255))")

# mycursor.execute("SHOW TABLES")

# for tb in mycursor:
#     print(tb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'This is dictionary argument',epilog = "Thanks for using")
    parser.add_argument('-l', '--link',nargs ='+',help="youtube url link")
    args = parser.parse_args()
    print(args)
    while(1):
        A = my_dictionary()
        list_of_links = []
        for values in vars(args):
            url_u = values,getattr(args,values)
            print(url_u)
            list_url = url_u[1]
            print(list_url)
            for get in list_url:
                 print(get)
                 list_of_links.append(A.check_video(get))
        for links in list_of_links:
            print(links)
            A.capt_download(links)
            list_of_words = A.caption_extract()
            for con in list_of_words:
               if A.check_db('dictionary','words',con) == False:
                   A.inser_value('dictionary','words',con)
                   A.new_word(con)
               else:
                   continue
    #    for el in elements:
    #        if len(el('a')) ==0:
    #            continue
    #        else:
    #            dlink = "https://www.youtube.com"+el('a')[0]["href"]
    #            links.append(dlink)
    #        if self.check_db(links[0]) == False:
    #            print("nothoing")
    #
    
    
    
    
            
