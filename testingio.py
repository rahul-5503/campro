import requests
from collections import Counter
import threading
import time
import os
import json

def get_ip_addresses():
       urls = [
        'https://api.ipify.org/',
        'https://checkip.amazonaws.com',
        'https://ipinfo.io/ip'
       ]
       ip_addresses = []
       for url in urls:
           try:
               response = requests.get(url)
               if response.status_code == 200:
                   #print("urls")
                   ip_addresses.append(response.text.strip())
           except Exception as e:
               print(f"Error retrieving IP address from {url}: {e}")
       best_ip=get_best_ip(ip_addresses)
       return best_ip
      
def get_best_ip(ip_addresses):         
       ip_counter = Counter(ip_addresses)#in the counter [ "12.145.23.45":2,"12.323.55.45":1]
       #best_ip store most common which has high number of count in["":2,"":1]
       best_ip = ip_counter.most_common(1)[0][0]
       return best_ip
         
def publicip():   
    #t1=threading.Thread(target=get_ip_addresses)
    #t1.start()
    oldip=0
    print("searching")
    while True:
       print("start")
       ip_addresses=get_ip_addresses()
       if ip_addresses == oldip:
            print("old IP address:",ip_addresses)
            #return True
       else:
         oldip=ip_addresses
         print('ip changed',oldip)
       time.sleep(180)
      
if __name__ == "__main__":
       publicip()
