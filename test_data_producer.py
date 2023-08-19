import json
import time
import pandas as pd
import requests

URL = 'http://127.0.0.1:5001/amex/stream/send_event'

def load_data():
     data = pd.read_csv(filepath_or_buffer='/Users/as/TanuProjects/amex_project/Test__dataset.csv', nrows=20)
     json_data = data.to_dict('records')
     for record in json_data:
         # print(record)
         start_time = time.time()
         response = requests.post(url=URL, json=record)
         print("Getting response from api- Status Code:", response.status_code, response.json())
         end_time = time.time()
         process_time = end_time - start_time
         print("process took {0} ms".format(process_time*10**3))
         time.sleep(1)

load_data()


