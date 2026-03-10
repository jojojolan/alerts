# get_red_alert.py
# Yonti
# Listen to the "alerts.json" 

import requests
import time
import os

OREF = r"https://www.oref.org.il/WarningMessages/alert/alerts.json"


r = requests.get(OREF)
r.encoding = 'utf-8-sig'

while r.status_code == 200:
    
    # there are alerts!
    if not r.text == '\r\n':
        print(r.json())
    else:
        print("Nothing Yet....")

    time.sleep(5)
    # Get the Json again
    r = requests.get(OREF)
    r.encoding = 'utf-8-sig'

