import string
import json
import time
import locale
import eel
import threading

from scapy.all import *
from apiclient import ApiClient


# disable scapy promiscuous mode
conf.sniff_promisc = 0


paths = {}
paused = False 


def mainloop(): 

    with open('config.json', 'r') as f:
        appconfig = json.load(f)

    apiclient = ApiClient(appconfig['apiurl'],appconfig['apikey'])

    lat  = 40.86577525616522
    long = 14.269432720014024

    loc = apiclient.get_location()            
    if loc is not None: 
        long = loc["longitude"]
        lat  = loc["latitude"]   

    while True:          
        coord = [long,lat]                 
        
        pkts = sniff(count=1,filter="")

        if not paused:
            if pkts[0].haslayer(TCP):    
                print("TCP ", pkts[0].payload.src, pkts[0].payload.dst)
                loc = apiclient.get_ip_location(pkts[0].payload.dst)            
                if loc is not None: 
                    ## print(pkts[0].payload.dst, loc["city"], loc["country_name"])               
                    coord.append(loc["longitude"])
                    coord.append(loc["latitude"])                
                    eel.updateData(coord,'tcp')
            elif pkts[0].haslayer(UDP):  
                print("UDP", pkts[0].payload.src, pkts[0].payload.dst)
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
                loc = apiclient.get_ip_location(pkts[0].payload.dst)            
                if loc is not None: 
                    ## print(pkts[0].payload.dst, loc["city"], loc["country_name"])               
                    coord.append(loc["longitude"])
                    coord.append(loc["latitude"])                
                    eel.updateData(coord,'udp') 

@eel.expose
def start_packet_capture():
    wd =  threading.Thread(target=mainloop, daemon=True)
    wd.start()

@eel.expose
def pause_packet_capture():
    global paused
    paused = not paused

@eel.expose
def save_config():
    global appconfig 
    with open('config.json', 'w') as f:
        json.dump(appconfig, f)

eel.init('web')
eel.start('main.html', size=(800, 1000))
