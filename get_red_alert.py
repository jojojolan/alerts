# get_red_alert.py
# Yonti
# Listen to the "alerts.json" 

import requests
import time
import logging
import json

# --- 1. Configure the Logger ---
# This sets up logging to output to BOTH the console and a file.
logging.basicConfig(
    level=logging.INFO, # Change to logging.DEBUG to see the "Nothing Yet..." messages
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("red_alert_monitor.log", encoding='utf-8'),
        logging.StreamHandler() # Keeps printing to the console
    ]
)

OREF = r"https://www.oref.org.il/WarningMessages/alert/alerts.json"
TEST_CITY = "יהוד-מונוסון"
alert_log_file_name = r"alert-0.json"

def monitor_alerts():
    logging.info("Starting Red Alert monitor...")
    
    while True:
        try:
            # Added a timeout so the script doesn't hang indefinitely 
            r = requests.get(OREF, timeout=10)
            r.encoding = 'utf-8-sig'
            
            if r.status_code == 200:

                if r.text.strip(): 
                    alert_data = r.json()
                    
                    # Log the alert to our system log
                    logging.warning(f"!! ALERT DETECTED: {alert_data}")
                    
                    # Append the raw JSON data to your specific data file
                    with open(alert_log_file_name, "a", encoding='utf-8') as f:
                        # Convert the dict back to a JSON string to write it
                        f.write(json.dumps(alert_data, ensure_ascii=False) + "\n")
                else:
                    # Logged as DEBUG so it doesn't spam your INFO logs
                    logging.debug("Nothing Yet....") 
            
            else:
                logging.error(f"Failed to fetch data. Status code: {r.status_code}")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        # Sleep before the next poll
        time.sleep(10)

if __name__ == "__main__":
    monitor_alerts()