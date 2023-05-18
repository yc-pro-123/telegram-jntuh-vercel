import requests ,os
import json , datetime
from clginfo import *
from sgpa_cal import *
from flask import Flask
from flask import request
from flask import Response
app = Flask('__name__')
BOT_TOKEN=os.getenv('BOT_TOKEN')
api=f'https://api.telegram.org/bot{BOT_TOKEN}'
def get_data(r_no):
    url=f'https://results-restapi.up.railway.app/all-r18/{r_no}'
    print('Getting Dataa.......')
    r=requests.get(url)
    return r
semre={
 '1-1': 1 , '1-2':2,'2-1':3,'2-2':4,'3-1':5,'3-2':6,'4-1':7,'4-2':8
    }   
semle={
'2-1':1,'2-2':2,'3-1':3,'3-2':4,'4-1':5,'4-2':6
}    
def _semlist(data,semno,mem):
    if(mem=='LE'):
        sem=semle
    else:
        sem=semre 
    q=data[semno - 1]
    #print(q) 
    #sgpa = q["SGPA"]
    res = q[list(sem.keys())[semno - 1]]
    #print(res)
    ar=list(res.keys())
    #ar=['15102','15103','15104','151AA','151AC','151AD','151AE']
    ls=[]    
    for each in ar:
        ls.append(res[each])
    #print(ls)
    return ls
  
def ls2txt(ls):
    stng= ''
    for u in range(len(ls)):
        stng= stng+ls[u]["subject_name"]+'\n'+' I : '+ls[u]["internal_marks"]+'         '+'E : '+ls[u]["external_marks"]+'\n'+'T : '+ls[u]['total_marks']+'        '+'G : '+ls[u]["grade_earned"]+'\n\n'
    return stng

def send_err(chat_id):
    method='/sendMessage'
    print(api+method)
    resp={'text':'Unsupported or Invalid Format \n Please try Again Later....','chat_id':chat_id }   
    r=requests.post(url=api+method,params=resp)
    return r.status_code

def fut_mess(chat_id):
    reso={'chat_id':chat_id,'text':"I can't Find any Data in my Database"   }
    
    send_mess(reso)
    resp={'chat_id':chat_id , 'text': "Are you trying to check future..? \U0001F60F \n\nIt seems like you didn't even wrote the exam"}
    send_mess(resp)

def action(chat_id):
    method='/sendChatAction'
    repo={'chat_id':chat_id,'action':'typing'}
    r=requests.post(url=api+method,params=repo)
    return r.status_code


def send_mess(resp):
    method='/sendMessage'
    #print(api+method)  
    #print('Message Sent...')
    r=requests.post(url=api+method,params=resp)
    
    return r.status_code
   
def parse_message(message):
   #print(message)
   chat_id=message["message"]["chat"]["id"]
   txt=message["message"]["text"]
   date=message["message"]["date"]
   nameby=message["message"]["from"]
   msg_id=message["message"]["message_id"]
   
   print('Chat_id :',chat_id,'\t',datetime.datetime.fromtimestamp(date))
   #print('User Id : '+nameby["username"])
print(nameby["first_name"]+'\t'+nameby["last_name"])
   print('Message Id :',msg_id,'\t\t',txt)
   return chat_id , txt ,msg_id

def wel_info(chat_id):
    resp ={ 'chat_id':chat_id,
    'text': "Hiii , Users....\nValid Format for using this bot are given Below : \n • ___20XXXAXXXX all___ - For All Sem Results\n • ___20XXXAXXXX 1-1___ - For Respective Sem\n • ___20XXXAXXXX 1-1 SGPA___  - For Finding SGPA of a Respective Sem\n• 20XXXAXXXX credits - For No of Credits Earned\n*Note* :\n *I* -- Internal Marks\n*E* -- External Marks\n*G* -- Grade Earned\n*T* -- Total Marks Earned\n\n<imp>Works *Only for R18* Regulation </imp>",'parse_mode': 'Markdown'
}   

    u= send_mess(resp)
    if u != 200:
        print('Wel_info Not sent\t Status :',u)
       
             
def roll_valid(rno,chat_id):
        br=['01','02','03','04','05','62','66','67','69','12']
        #print(rno[6:8])
        if(br.count(rno[6:8])!=0 and len(rno)==10):
            #print('Hiiiii')
            return 'OK'
        
def roll_mem(rno):
                   if(rno[4:6] == '1A'):
                       mem='REG'
                   elif(rno[4:6]=='5A'):
                       mem='LE'
                   else:
                       mem='UNKNOWN'
                   return mem       
  
                                    
@app.route('/',methods=["POST" ,"GET"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        #print(msg,'\n')
        try:
            chat_id , txt ,msg_id = parse_message(msg)
        except:            
            return Response(status=200)
        
        #print(chat_id,txt)  
        if(txt == '/start'):
            wel_info(chat_id)
            return Response('OK',status=200 )
        if(txt =='/contact'):
            action(chat_id)
            send_mess({'chat_id':chat_id,'text':'\nFor further Queries or Issues Contact Us !\nAdmin : @y_c_pro\nCo-Admin : @K_N_R_P \nMade with Love towards Friends'})
            return Response(status=200)
        
        if(txt =='/about'):
            action(chat_id)
            send_mess({'chat_id':chat_id,'text':'\n\nThis is a Mini bot started for my mini gang which can find *JNTUH* Results of *R18 Regulation* Number \U0001F9BE \n\nHope it will helpful for you too. \U0001F609\nSuggest any *Features* you wish which this bot may consist of........\nFeedbacks are *Most Welcomed*....\n\nMade with Love \U0001F496 for my Friends','parse_mode':'Markdown'})
            return Response(status=200)
        
        
        try:
            rno,sel = txt.strip().split(' ',1)
        except:
            print('Returning Response Okk.....')
            wel_info(chat_id)           
            return Response('OK',status =200)
        sel=sel.upper()
        if roll_valid(rno,chat_id) !='OK':
            send_mess({'chat_id':chat_id,'text':'Seems like its a Invalid Number \nPlz ,Try again with a Valid Number.....'})
            return Response('OK',status =200)
        
        mem = roll_mem(rno)
        if(mem=='LE'):
            sem=semle
        else:
            sem=semre
        r18=['18','19','20','21']
        if rno[:2]  in r18:
            pass
        else:
            action(chat_id)
            repo={'chat_id':chat_id,'text':'This Bot only works or Process R18 Students Info \nSo Kindly Enter a R18 Number \U0001F604'}
            send_mess(repo)
            return Response(status=200)
        v=get_data(rno.upper());
        #print(v.text)
        i=json.loads(v.content)
        try:
            details=i["data"]["details"]
        except:
            action(chat_id)
            send_mess({'chat_id':chat_id,'text':'Seems like its a Invalid Number \nPlz Try again Later','reply_to_message_id':msg_id})
            return Response('OK',status =200)
        data=i["data"]["results"]            
        semc=len(data)
        
        if(sel =='D'):
            action(chat_id)
            clg = getclg(details['COLLEGE CODE'])
            try:
                text=details['HTNO']+'\n'+details['NAME']+'\n\n'+clg['C_name']+'\n'+clg['Code']+'\n'+clg['City']
            except:
                text="Think There's a Problem...."
            
            repo={
            'chat_id':chat_id,
            'text':text,'reply_to_message_id':msg_id,'protect_content':True}
            send_mess(repo)            
            return Response(status=200)    
                
        if(sel=='CREDITS' or sel =='CREDIT'):
            action(chat_id)
            try:
                cred=0
                print('Credits startedd...')
                for w in range(1,len(data)+1,1):
                    print('Sem No : ',w)
                    listt= _semlist(data,w,mem)
                    try:
                        cred+=noofcreds(listt)
                    except:
                        return Response(status=200)
                txt=f'Credits Earned by Entered number is : {cred}'
                repo={'chat_id':chat_id ,'text':txt}
                print('sending credit Infoo')
                send_mess(repo)
                return Response(status=200)
            except:
                repo={'chat_id':chat_id,'text':'Error Occured while finding Credits, please try again later.......'}
                send_mess(repo)
                return Response(status=200)
        
        if(sel=='F' or sel =='AB' or sel =='FAIL'):
            action(chat_id)
            try:
                f,ab,ab1,f1=0,0,0,0
                print('No of Backlogs startedd...')
                for w in range(1,len(data)+1,1):
                    print('Sem No : ',w)
                    listt= _semlist(data,w,mem)
                    try:
                        f1,ab1=nooffail(listt)
                        f=f+f1
                        ab=ab+ab1
                    except:
                        return Response(status=200)
                txt=f'No of Backlogs for Entered number is : {int(f)+int(ab)}\nFailed : {f}\nNo. of Absentee : {ab}'
                if f==0:
                    txt+='\n\nNice !\nLooks like a Topper !!'
                repo={'chat_id':chat_id ,'text':txt}
                print('Sending Backlog Infoo')
                send_mess(repo)
                return Response(status=200)
            except:
                repo={'chat_id':chat_id,'text':'Error Occured while finding Number of Backlogs , please try again later.......'}
                send_mess(repo)
                return Response(status=200)
        

        if(sel[:3]=='ALL'):
            action(chat_id)
            try:
                print('All startedd...',end="\r")
                for w in range(1,len(data)+1,1):
                    #print('Sem No : ',w)
                    
                    listt= _semlist(data,w,mem)
                    #print(sgpa(listt))
                    if(len(sel)==3):
                        a=list(sem.keys())[w - 1]
                        txt=f"----------{a}----------\n"
                        txt+=ls2txt(listt)
                        print('Processing',list(sem.keys())[w-1],end="\r")
                        try:
                            
                            r=sgpa(listt)
                            if(isinstance(r,float)):
                                txt+='Yours SGPA in '+list(sem.keys())[w-1]+' is '+str(r)
                            else:
                                txt+='Sorry ! Cant find your SGPA'                   
                        except:                          
                            txt+='Sorry ! Cant find your SGPA'
                        repo={'chat_id':chat_id,'text':txt}
                        send_mess(repo)
                    elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                        try:
                            r=sgpa(listt)
                            if(isinstance(r,float)):
                                txt='Yours SGPA in '+list(sem.keys())[w-1]+' is '+str(r)
                            else:
                                txt='Sorry ! Cant find your SGPA'                   
                        except:                          
                            txt='Sorry ! Cant find your SGPA'
                        repo={'chat_id':chat_id,'text':txt}
                        send_mess(repo)
                    else:
                        send_err(chat_id)
                
                print('All Completed .....')
                send_mess({'chat_id':chat_id,'text':'.......Request\n          Accomplished......'})
                #send_mess({'chat_id':chat_id,'text':'\nFor a Soft Copy of Result [click here](https://t.me/Ucdgdgvou_bot?start={rno}','parse_mode':'Markdown'})
            except:
                repo={'chat_id':chat_id,'text':'Looks like Something Went wrong......\nPlease try again Later'}
                send_mess(repo)
                return Response(status=200)
            
            
            
            
#1-1 Processs        
        
        if(sel[:3]=='1-1'):
            action(chat_id)
            if(mem=='LE'):
                resp={'chat_id':chat_id,'text':'Please Check the Entered Input\nAs I know a Lateral Entry Person will Join their B.tech directly in 2-1.\nBut you seems like Asking 1-1 and 1-2 Sem which seems like impossible.........'}
                
                send_mess(resp)
                return Response(status=200)
            else:
                if(sem[sel[:3]] <= semc):
                    listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                    if(len(sel) == 3):
                        txt=ls2txt(listt)
                        try:
                            r=sgpa(listt)
                            if(isinstance(r,float)):
                                txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                            else:
                                txt+="Can't able to Find SGPA"
                        except:
                            txt+='Sorry Cant find You SGPA'
                        repo={'chat_id':chat_id ,'text':txt,'reply_to_message_id':msg_id}
                        send_mess(repo)
                    elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                        try:
                            r=sgpa(listt)                        
                            if(isinstance(r,float)):
                                txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                            else:
                                txt+="Can't able to Find SGPA"
                        except:
                            txt='Sorry Cant find You SGPA'

                        repo ={ 'chat_id':chat_id, 'text' :txt ,'reply_to_message_id':msg_id}
                        send_mess(repo)
                    else:
                        send_err(chat_id)
                else:
                    fut_mess(chat_id)
                    return Response(status=200)

#1-2 Processssss   
        if(sel[:3]=='1-2'):
            if(mem=='LE'):
                action(chat_id)
                resp={'chat_id':chat_id,'text':'Please Check the Entered Input\nAs I know a Lateral Entry Person will Join their B.tech directly in 2-1.\nBut you seems like Asking 1-1 and 1-2 Sem which seems like impossible.........'}
                
                send_mess(resp)
                return Response(status=200)
            else:
                if(sem[sel[:3]] <= semc):
                    action(chat_id)
                    listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                    if(len(sel) == 3):
                        txt=ls2txt(listt)
                        try:
                            r=sgpa(listt)
                        
                            if(isinstance(r,float)):
                                txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                            else:
                                txt+="Can't able to Find SGPA"
                        except:
                            txt+='Sorry Cant find You SGPA'
                        repo={'chat_id':chat_id ,'text':txt,'reply_to_message_id':msg_id}
                        send_mess(repo)
                    elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                        try:
                            r=sgpa(listt)
                        
                            if(isinstance(r,float)):
                                txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                            else:
                                txt+="Can't able to Find SGPA"
                        except:
                            txt='Sorry Cant find You SGPA'

                        repo ={ 'chat_id':chat_id, 'text' :txt ,'reply_to_message_id':msg_id}
                        send_mess(repo)
                    else:
                        send_err(chat_id)
                else:
                    fut_mess(chat_id)
                    return Response(status=200)

#2-1 Processss        
        if(sel[:3]=='2-1'):
            if(sem[sel[:3]] <= semc):
                action(chat_id)
                listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                if(len(sel) == 3):
                    txt=ls2txt(listt)
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt+='Sorry Cant find You SGPA'
                    repo={'chat_id':chat_id ,'text':txt,'reply_to_message_id':msg_id}
                    send_mess(repo)
                elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except: 
                        txt='Sorry Cant find You SGPA'

                    repo ={ 'chat_id':chat_id, 'text' :txt ,'reply_to_message_id':msg_id}
                    send_mess(repo)
                else:
                    send_err(chat_id)
            else:
                fut_mess(chat_id)
                return Response(status=200)

#2-2 Processsssss        
        if(sel[:3]=='2-2'):
            if(sem[sel[:3]] <= semc):
                action(chat_id)
                listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                if(len(sel) == 3):
                    txt=ls2txt(listt)
                    try:
                        r=sgpa(listt)                  
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt+='Sorry Cant find You SGPA'
                    repo={'chat_id':chat_id ,'text':txt,'reply_to_message_id':msg_id}
                    send_mess(repo)
                elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt='Sorry Cant find You SGPA'

                    repo ={ 'chat_id':chat_id, 'text' :txt,'reply_to_message_id':msg_id}
                    send_mess(repo)
                else:
                    send_err(chat_id)
            else:
                fut_mess(chat_id)
                return Response(status=200)
#3-1 Processss        
        if(sel[:3]=='3-1'):
            if(sem[sel[:3]] <= semc):
                action(chat_id)
                listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                if(len(sel) == 3):
                    txt=ls2txt(listt)
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt+='Sorry Cant find You SGPA'
                    repo={'chat_id':chat_id ,'text':txt,'reply_to_message_id':msg_id}
                    send_mess(repo)
                elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except: 
                        txt='Sorry Cant find You SGPA'

                    repo ={ 'chat_id':chat_id, 'text' :txt,'reply_to_message_id':msg_id }
                    send_mess(repo)
                else:
                    send_err(chat_id)
            else:
                fut_mess(chat_id)
                return Response(status=200)

#3-2 Processss        
        if(sel[:3]=='3-2'):
            if(sem[sel[:3]] <= semc):
                action(chat_id)
                listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                if(len(sel) == 3):
                    txt=ls2txt(listt)
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt+='Sorry Cant find You SGPA'
                    repo={'chat_id':chat_id ,'text':txt,'reply_to_message_id':msg_id}
                    send_mess(repo)
                elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                    try:
                        r=sgpa(listt)                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt='Sorry Cant find You SGPA'

                    repo ={ 'chat_id':chat_id, 'text' :txt,'reply_to_message_id':msg_id}
                    send_mess(repo)
                else:
                    send_err(chat_id)
            else:
                fut_mess(chat_id)
                return Response(status=200)

#4-1 Processss      
        if(sel[:3]=='4-1'):
            action(chat_id)
            if(sem[sel[:3]] <= semc):
                
                listt= _semlist(data,sem[sel[:3]],mem)
                #enters if a valid sem for roll number
                if(len(sel) == 3):
                    txt=ls2txt(listt)
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt+='Sorry Cant find You SGPA'
                    repo={'chat_id':chat_id ,'text':txt}
                    send_mess(repo)
                elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                    try:
                        r=sgpa(listt)
                    
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt='Sorry Cant find You SGPA'

                    repo ={ 'chat_id':chat_id, 'text' :txt }
                    send_mess(repo)
                else:
                    send_err(chat_id)
            else:
                fut_mess(chat_id)
                return Response(status=200)

        
        
   

#4-2 Processss        
        if(sel[:3]=='4-2'):
            action(chat_id)
            if(sem[sel[:3]] <= semc):
                
                listt= _semlist(data,sem[sel[:3]],mem)
                if(len(sel) == 3):
                    txt=ls2txt(listt)
                    try:
                        r=sgpa(listt)
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt+='Sorry Cant find You SGPA'
                    repo={'chat_id':chat_id ,'text':txt}
                    send_mess(repo)
                elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
                    try:
                        r=sgpa(listt)
                        if(isinstance(r,float)):
                            txt+="Your's SGPA in "+sel[:3] +" is "+str(r)
                        else:
                            txt+="Can't able to Find SGPA"
                    except:
                        txt='Sorry Cant find You SGPA'
                    repo ={ 'chat_id':chat_id, 'text' :txt }
                    send_mess(repo)
                else:
                    send_err(chat_id)
            else:
                resp={'chat_id':chat_id,'text':" I wish i could process your request , but I can't Go ahead in time and Grab your Result......\n\nIf Incase I can , then I would like to bring you the Question Papers either than Results"}
                send_mess(resp)
                return Response(status=200)   
       
        
        return Response('OK', status = 200)
    else:
        return '<h1>Hii JNTUH RESULTS</h1>'          
        
        
        
def main():    
    #print('started')
    k='    20UJ1A0412 2-1 '
    rno=input('Enter the Number :')
    #rno,sel = txt.strip().split(' ',1)
    #semno=int(input('Enter Sem No :'))
    v=get_data(rno);
    i=json.loads(v.content)    
    #print(json.dumps(i,indent=1))
    details=i["data"]["details"]
    #print(details)
    data=i["data"]["results"]
    print(details)
    print(getclg(details['COLLEGE CODE']))
    print(details['NAME'],details['HTNO'])
    semc=len(data)
    print('No of Sems Completed : ',len(data))
    #print(data)
    #print(data[2]["2-1"])
    typeroll=roll_mem(rno)
    if(typeroll=='LE'):
        sem=semle
    else:
        sem=semre
    rno,sel=k.strip().split(' ',1)
    print(sel[4:])
    if(sel[:3] == '2-1'):
        if(len(sel) == 3):
            print(' Length of sel is 3')
        elif(len(sel)== 8 and sel[4:].upper() =='SGPA'):
            print(' Found  SGPA')
        else:
            print('error')
        #print('1-111111')
    #ee="Your's SGPA in "+sel[:3] +" is "+str(sgpa(listt))
    #print(ee)
    #j .  !!!!!!!;;;+::%%6send_err()
    
#flask --app hello --debug run
#if __name__ =='__main__':
    #app.run(debug=True)
    #main()
