import time
from time import gmtime, strftime
from datetime import datetime
import telepot
import string
from telepot.loop import MessageLoop
import re
import random
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://<username>:<password>@cluster0.oylmd.mongodb.net/<database>?retryWrites=true&w=majority")
#username is mongodb atlas username
#password is database/mongodb atlas password
#database is the database name, in this case, wakeup
db=cluster["wakeup"]
col1=db["users"] #which collection you want to use
usertime=0
usid=0
now=datetime.now()
validtime=0
start=datetime.now()
num1=0
num2=0
ans=-1
crepic=0
x=-1
uname=""
logged_user=""
setStatus=0
perUserTime=""
setUser=""
checkRegUser=0
checkRegId=0
checkLoggedUser=0
validateCrepic=0
validateProperTime=0
validateUserId=0
validateCorName=""
validateMatch=0

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    global usertime
    global now
    global usid
    global crepic
    global num1
    global num2
    global ans
    global x
    global uname
    global logged_user
    global db
    global col1
    global col2
    global setStatus
    global perUserTime
    global setUser
    global checkRegUser
    global checkLoggedUser
    global validateCrepic
    global checkRegId

    print(chat_id)

    usid = chat_id

    if command == "/help":
        WakeMeUpPlsbot.sendMessage(chat_id,str("REMINDER THAT THIS BOT USES ASIA/SINGAPORE TIMEZONE. ONE TELEGRAM ACCOUNT CAN ONLY REGISTER ONE ACCOUNT \n Use /reg followed by a username to register your username. Example: /reg firdauskotp \n Use /login followed by the username you registered to use most of this bot's functions. Example: /login firdauskotp \nUse /alarm followed by the time in 24 hour format and : in the middle to set the alarm time to be spammed! Example: /alarm 01:30 \n Use /clear to clear the time you input \n Use /curtime to know the current time in Asia/Singapore timezone \n Use /curalarm to show the alarm you saved \n Want to go further? use /creepypicon to include an image. If you change your mind, use /creepypicoff. By default it is off \n Want to stop the alarm? Answer the math question given by using /curans followed by the answer"))
    elif command == "/start":
        WakeMeUpPlsbot.sendMessage(chat_id,str("Welcome! REMINDER THAT THIS BOT USES ASIA/SINGAPORE TIMEZONE. ONE TELEGRAM ACCOUNT CAN ONLY REGISTER ONE ACCOUNT \n Use /help to know what commands to use \n If you don't have an account, please use /reg followed by a username of your choice first. \n If you have registered, use /login followed by the username you registered to use the alarm"))
        WakeMeUpPlsbot.sendPhoto(chat_id,photo="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Fpb59vnz6zgk51.jpg&f=1&nofb=1")
    elif command == "/curtime":
        WakeMeUpPlsbot.sendMessage(chat_id,strftime("%H:%M"))
    elif command.find("/reg") != -1:
        l=3
        if len(command[0+l+1:])==0:
            WakeMeUpPlsbot.sendMessage(chat_id,str("Please insert a username"))
        else:
            uname=command[0+l+1:].strip()
            unameQuery = col1.find({"name":uname})

            idQuery = col1.find({"_id":chat_id})

            checkRegUser=0
            checkRegId=0

            for getRegUser in unameQuery:
                checkRegUser+=1

            for getRegID in idQuery:
                checkRegId+=1

            if checkRegUser==0 and checkRegId==0:
                post_user = {"_id":chat_id,"name":uname, "time": 0,"creepypic":0,"match":0}
                col1.insert_one(post_user)
                WakeMeUpPlsbot.sendMessage(chat_id,str("Username registered!"))
            else:
                WakeMeUpPlsbot.sendMessage(chat_id,str("Username is taken or there is an account on your current Telegram account! Please use another username"))

    elif command.find("/login") != -1:
        l=5
        if len(command[0+l+1:])==0:
            WakeMeUpPlsbot.sendMessage(chat_id,str("Please insert a username"))
        else:
            logged_user=command[0+l+1:].strip()
            lunameQuery=col1.find({"name":logged_user})

            checkLoggedUser=0

            for gettingloggingusers in lunameQuery:
                checkLoggedUser+=1
                
            
            if checkLoggedUser>0:
                WakeMeUpPlsbot.sendMessage(chat_id,str("You are now logged in! You can use the full functions of the bot"))
                setStatus = 1
                # setUser=logged_user
            else:
                WakeMeUpPlsbot.sendMessage(chat_id,str("The username is not registered. Please review it or register a new username"))
    #for logged in users
    elif command == "/curalarm" and setStatus==1:
        
        if usertime ==0:
            WakeMeUpPlsbot.sendMessage(chat_id,str("You did not set an alarm!"))
        else:
            # WakeMeUpPlsbot.sendMessage(chat_id,usertime)
            results = col1.find({"_id":chat_id})
            for getTime in results:
                # if getTime["time"]=="00:00":
                #     WakeMeUpPlsbot.sendMessage(chat_id,str("You did not set an alarm!"))
                # else:
                WakeMeUpPlsbot.sendMessage(chat_id,getTime["time"])
    elif command.find("/curans") != -1 and setStatus==1:
        l=6
        if len(command[0+l+1:])==0:
            WakeMeUpPlsbot.sendMessage(chat_id,str("Please provide an answer after /curans"))
        else:  
            ans = command[0+l+1:].strip()
            x=int(ans)
            # WakeMeUpPlsbot.sendMessage(chat_id,str("Answer stored"))
    elif command == "/clear" and setStatus==1:
        usertime = 0
        WakeMeUpPlsbot.sendMessage(chat_id,str("Alarm resetted!"))
        col1.update_one({"_id":chat_id}, {"$set":{"time": 0}})
    elif command == "/creepypicon" and setStatus==1:
        # crepic=1
        col1.update_one({"_id":chat_id}, {"$set":{"creepypic": 1}})
        WakeMeUpPlsbot.sendMessage(chat_id,str("You have a terrible fate ahead"))
    elif command == "/creepypicoff" and setStatus==1:
        # crepic=0
        col1.update_one({"_id":chat_id}, {"$set":{"creepypic": 0}})
        WakeMeUpPlsbot.sendMessage(chat_id,str("Coward :p"))
        
    elif command.find("/alarm") != -1 and setStatus==1:
        l=5
        if len(command[0+l+1:])==0:
            WakeMeUpPlsbot.sendMessage(chat_id,str("Example of using the alarm \n /alarm 15:30"))
        else:
            zone = command[0+l+1:].strip()
            if re.search('[a-zA-Z]',zone):
                WakeMeUpPlsbot.sendMessage(chat_id,str("Letters detected! Only numbers please"))
            else:
                if re.search(r'\d',zone):
                    if len(zone)>5:
                        WakeMeUpPlsbot.sendMessage(chat_id,str("Invalid time"))
                    elif len(zone)==5 and zone[2]!=":":
                        WakeMeUpPlsbot.sendMessage(chat_id,str("Invalid time"))

                    elif len(zone)==4 and zone[1]==":":
                        usertime = "0"+str(zone[0])+":"+str(zone[2])+str(zone[3])
                        WakeMeUpPlsbot.sendMessage(chat_id,str("Alarm saved!"))
                        #WakeMeUpPlsbot.sendMessage(chat_id,str(usertime))
                        num1 = random.randint(0,100)
                        num2 = random.randint(0,100)
                        # perUserTime = {"name":uname}, {"$set":{"time": usertime}}
                        col1.update_one({"_id":chat_id}, {"$set":{"time": usertime}})
                        

                    elif len(zone)==4 and zone[2]!=":":
                        usertime = str(zone[0]) + str(zone[1]) + ":" + str(zone[2]) + str(zone[3])
                        WakeMeUpPlsbot.sendMessage(chat_id,str("Alarm saved!"))
                        #WakeMeUpPlsbot.sendMessage(chat_id,str(usertime))
                        num1 = random.randint(0,100)
                        num2 = random.randint(0,100)
                        # perUserTime = {"name":uname}, {"$set":{"time": usertime}}
                        col1.update_one({"_id":chat_id}, {"$set":{"time": usertime}})
                    elif len(zone)<=3:
                        WakeMeUpPlsbot.sendMessage(chat_id,str("Invalid time"))
                    else:
                        WakeMeUpPlsbot.sendMessage(chat_id,str("Alarm saved!"))
                        usertime = str(zone)
                        #WakeMeUpPlsbot.sendMessage(chat_id,str(usertime))
                        num1 = random.randint(0,100)
                        num2 = random.randint(0,100)
                        # # # perUserTime = {"name":uname}, {"$set":{"time": usertime}}
                        col1.update_one({"_id":chat_id}, {"$set":{"time": usertime}})
                        
                else:
                    WakeMeUpPlsbot.sendMessage(chat_id,str("Letters detected! Only numbers please"))
    elif setStatus==0 and command == "/curalarm" or command.find("/curans") != -1 or command == "/clear" or command == "/creepypicon" or command == "/creepypicoff" or command.find("/alarm") != -1:
        WakeMeUpPlsbot.sendMessage(chat_id,str("You are not logged in!"))
    else:
        WakeMeUpPlsbot.sendMessage(chat_id,str(now.strftime("Wrong command, use /help to see available commands")))
  
#token
WakeMeUpPlsbot = telepot.Bot('paste your bot token here')
print (WakeMeUpPlsbot.getMe())

#Calling function
WakeMeUpPlsbot.message_loop({'chat':action})
#WakeMeUpPlsbot.setWebhook()
#pause

while 1:

    #validtime = now.strftime("%H:%M")
    validtime = strftime("%H:%M")

    idArray=[]
    timeArray=[]
    creepypicArray=[]
    matchArray=[]

   
    results = col1.find({})
    for getComparisonTime in results:
        validateProperTime=getComparisonTime["time"]
        validateCrepic=getComparisonTime["creepypic"]
        validateUserId=getComparisonTime["_id"]
        validateCorName=getComparisonTime["name"]
        validateMatch=getComparisonTime["match"]
        idArray.append(validateUserId)
        timeArray.append(validateProperTime)
        creepypicArray.append(validateCrepic)
        matchArray.append(validateMatch)

    for fullValidation in range(len(idArray)):
        if timeArray[fullValidation]==validtime or matchArray[fullValidation]==1:
            col1.update_one({"_id":idArray[fullValidation]}, {"$set":{"match": 1}})
            # while True:
                
            WakeMeUpPlsbot.sendMessage(idArray[fullValidation],str("WAKE UP! WANT TO STOP? ANSWER THE QUESTION \n " + str(num1) + " + " + str(num2) + "\n YOU SHOULD BE AWAKE NOW I HOPE"))
            
            if creepypicArray[fullValidation]==1:
                WakeMeUpPlsbot.sendPhoto(idArray[fullValidation], photo="https://i.pinimg.com/originals/67/0f/44/670f448418af63954c5dc20bc7932754.jpg")
            else:
                pass
            
            if int(num1)+int(num2) == int(x):
                # print("loop break")
                # usertime=0
                # validateProperTime=0
                col1.update_one({"_id":idArray[fullValidation]}, {"$set":{"match": 0, "time": 0}})
                WakeMeUpPlsbot.sendMessage(usid, str("YOU ARE FREE NOW"))
                x = -1
                
            elif x==-1:
                pass
            else:
                WakeMeUpPlsbot.sendMessage(validateUserId, str(x) + " IS WRONGGGGGGG")
                x = -1
    
    idArray.clear()
    timeArray.clear()
    creepypicArray.clear()
    matchArray.clear()
                
    time.sleep(1)
