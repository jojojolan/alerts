# get_red_alert.py
# Yonti
# Listen to the "alerts.json" 

import requests
from time import sleep
import logging
import json

# This sets up logging to output to BOTH the console and a file.
logging.basicConfig(
    level=logging.INFO, # Change to logging.DEBUG to see the "Nothing Yet..." messages
    # level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("red_alert_monitor.log", encoding='utf-8'),
        logging.StreamHandler() # Keeps printing to the console
    ]
)

OREF = r"https://www.oref.org.il/WarningMessages/alert/alerts.json"
alert_log_file_name = r"alerts.json"

def monitor_alerts(prev_alert_id: str):  
   
    try:
        # Added a timeout so the script doesn't hang indefinitely 
        r = requests.get(OREF, timeout=10)
        r.encoding = 'utf-8-sig'
        
        if r.status_code == 200:

            if r.text.strip(): 
                alert_data = r.json()

                # Checks for the same Id
                if alert_data["id"] == prev_alert_id:
                    logging.info("Still the Same alert ID...")
                    return 
                
                alert_dump = {field: alert_data[field] for field in ["id","cat","title","data"]}
                
                # Log the alert to our system log
                logging.warning(f"!! ALERT DETECTED: {alert_dump["title"]}")
                
                # Append the raw JSON data to your specific data file
                with open(alert_log_file_name, "a", encoding='utf-8') as f:
                    # Convert the dict back to a JSON string to write it
                    f.write(json.dumps(alert_dump, ensure_ascii=False) + "\n")
                    return alert_dump
            else:
                # Logged as DEBUG so it doesn't spam your INFO logs
                logging.debug("Nothing Yet....") 
        
        else:
            logging.error(f"Failed to fetch data. Status code: {r.status_code}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    

def send_check(alerts_list: list):
    """Send Whatsapp DM to however is in the city list"""
    pass

def main():
    logging.info("Starting Red Alert monitor...")
    alert_id = "42"
    while True:
        alerts = monitor_alerts(alert_id)
        
        # if alerts:
        #     alert_id = alerts["id"]
            
        #     # ירי רקטות וטילים or חדירת כלי טיס עוין
        #     if alerts["cat"] in ["1","6"]:
        #         send_check(alerts["data"])
        #         pass

        #     elif alerts["cat"] == "10":
        #         logging.info("Alert Ended")
        sleep(10)


if __name__ == "__main__":
    main()