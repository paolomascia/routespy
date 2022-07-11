import requests
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus

import sqlite3 as sl

APIKEY = "b3cb43a02d0d41b3bb65c76a54d4857d"
APIURL = "https://api.ipgeolocation.io/ipgeo"

class ApiClient:
    
    def __init__(self):
        self.conn = sl.connect("ipdb.db", check_same_thread=False)
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS ipdb (
                ip TEXT PRIMARY KEY,
                apiresponse TEXT)
            """)

    def get_ip_location(self,ip):

        r = self.conn.execute("SELECT * FROM ipdb WHERE ip = ?",(ip,)).fetchone()
        if r is not None:
            if r[1] is not None:
                return json.loads(r[1])
            else:
                return None

        url = APIURL
        params = dict(
            apiKey=APIKEY,
            ip=ip
        )
        resp = requests.get(url=url, params=params)
        data = resp.json()  
        if 'latitude' in data.keys() and 'longitude' in data.keys():
            apiresponse = resp.text       
            self.conn.execute("INSERT INTO ipdb (ip,apiresponse) VALUES (?,?)",(ip,apiresponse))    
            self.conn.commit() 
        else:
            apiresponse = None
            data = None 
            self.conn.execute("INSERT INTO ipdb (ip,apiresponse) VALUES (?,NULL)",(ip,))    
            self.conn.commit() 
        
        return data
    
    def get_location(self):
        url = APIURL
        params = dict(
            apiKey=APIKEY
        )
        resp = requests.get(url=url, params=params)
        data = resp.json() 
        if 'latitude' in data.keys() and 'longitude' in data.keys():
           return data
        else:
           return None