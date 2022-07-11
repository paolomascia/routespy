import string
import json
import time
import locale
import eel
import threading

from scapy.all import *
from apiclient import ApiClient

apiclient = ApiClient()
paths = {}

def mainloop():   
    
    lat = 40.86577525616522
    long = 14.269432720014024

    loc = apiclient.get_location()            
    if loc is not None: 
        long = loc["longitude"]
        lat  = loc["latitude"]   

    while True:          
        coord = [long,lat]                 
        
        pkts = sniff(count=1,filter="tcp and dst 192.168.1.9")
        print("Adding route to", pkts[0].payload.src)

        '''
        result, unans = traceroute(pkts[0].payload.src,maxttl=32)
        for snd,rcv in result:
            loc = apiclient.get_ip_location(rcv.src)            
            if loc is not None: 
                print(rcv.src, loc["city"], loc["country_name"])               
                coord.append(loc["longitude"])
                coord.append(loc["latitude"])                
        eel.updateData(coord)
        '''
        loc = apiclient.get_ip_location(pkts[0].payload.src)            
        if loc is not None: 
            print(pkts[0].payload.src, loc["city"], loc["country_name"])               
            coord.append(loc["longitude"])
            coord.append(loc["latitude"])                
        eel.updateData(coord)

@eel.expose
def start_packet_capture():
    wd =  threading.Thread(target=mainloop, daemon=True)
    wd.start()
  
eel.init('web')
eel.start('main.html', size=(800, 1000))
