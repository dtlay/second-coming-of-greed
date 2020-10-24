import re
import sys
import warnings
import json
import string
import random
import urllib
from bs4 import BeautifulSoup
import ssl
import requests
import json
#import websocket
# warnings.filterwarnings("ignore")
# ssl._create_default_https_context = ssl._create_unverified_context
# requests.packages.urllib3.disable_warnings()


baseuri = "https://www.wuxiaworld.com/"

loginuri = "https://www.wuxiaworld.com/account/login"

scoguri = "https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony/scog-chapter-%s"

login_headers = { # login_headers start
    'authority': 'www.wuxiaworld.com'  
  , 'cache-control' : 'max-age=0'  
  , 'dnt': '1'  
  , 'upgrade-insecure-requests': '1'  
  , 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36'  
  , 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'  
  , 'sec-fetch-site': 'same-origin'  
  , 'sec-fetch-mode': 'navigate'  
  , 'sec-fetch-dest': 'document'  
  , 'referer': 'https://www.wuxiaworld.com/'  
  , 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'  
} # login_headers end

login_post_values = {
        "Email": "REPLACE_ME",
        "Password": "REPLACE_ME",
        "__RequestVerificationToken": "GENERATED_TOKEN",
        "RememberMe": "false"
}

def scog_chapter(uname,passwd,chapterid=None):

    with requests.Session() as sess:
        soup = BeautifulSoup(sess.get(loginuri, headers=login_headers, allow_redirects=True).content, 'html.parser')
        request_verification_token = soup.find("input", attrs={"name":"__RequestVerificationToken"}).get("value")
        print(request_verification_token)

        if request_verification_token:
            login_post_values["__RequestVerificationToken"] = request_verification_token
            login_post_values["Email"] = uname
            login_post_values["Password"] = passwd
            resp = sess.post(loginuri, data=login_post_values, headers=login_headers, allow_redirects=True)

            if (resp.ok):
                wxw_chapter_uri = scoguri % (str(chapterid))
                print(wxw_chapter_uri)
                soup = BeautifulSoup(sess.get(wxw_chapter_uri, headers=login_headers).content, 'html.parser', from_encoding='utf8')
                soup.prettify("latin-1")
                title = soup.find_all('h4')[1].text
                content = soup.find_all('p')
                story = {}
                story['cid'] = str(chapterid)
                story['title'] = title
                story['content'] = [] 

                badstr = ["RSS", 
                        "Twitter", 
                        "Facebook", 
                        "Discord", 
                        "Privacy Policy", 
                        "Contact Us", 
                        "Copyright", 
                        "Ro Yu-Jin", 
                        "================="]

                index = 0
                for line in content:
                    badfound = False
                    for bs in badstr:
                        if bs in line.text:
                            badfound = True
                    if badfound == True:
                        content = content[:index]
                        break
                    index += 1

                [ story['content'].append(line.text) for line in content ]
                

                with open("../chapters/scog-%s.json" % chapterid, 'w')  as outfile:
                    json.dump(story,outfile)

            

if __name__ == "__main__":
    uname, passwd = "user@email.com.com", "PASSWORD"
    for x in range(1, 473):
        uri = scog_chapter(uname, passwd, str(x))
        print(uri)
        import time
        time.sleep(5)
