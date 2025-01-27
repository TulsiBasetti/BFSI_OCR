"""
Account Statement Fetching & Saving

- API Request: Sends a POST request to Axis Bank API for account statement.
- Headers: Includes necessary authentication and service information for the request.
- Error Handling: Catches any request exceptions and prints error messages if the request fails.
- JSON Response: Saves the response from the API as a JSON file to local storage.
- Data Processing: Reads the saved JSON file into a pandas DataFrame for further analysis.
"""

import requests
import json
import pandas as pd

def get_account_statement():
    url = "https://apiportal.axisbank.com/gateway/neobanking/api/v1/account-statement-report"
    
    headers = {
        "Accept": "application/json",
        "X-IBM-Client-Id": "3607c737c837d935f44c8f2d95501f65",
        "X-IBM-Client-Secret": "680f9b350fd1df0a1dbec231dd9c0aad",
        "x-fapi-epoch-millis": "zirivmumuhi",
        "x-fapi-channel-id": "121863566802944",
        "x-fapi-uuid": "59717040314776",
        "x-fapi-serviceid": "8951335418331136",
        "x-fapi-serviceVersion": "wuhv",
        "X-AXIS-TEST-ID": "1"
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json() # Will raise an exception if the status code is 4xx or 5xx
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

if __name__ == "__main__":
    result = get_account_statement()
    if result:
        try:
            with open('C:\\Infosys_Springboard_Internship\\Data\\statement.json','w') as json_file:
                json.dump(result,json_file,indent=4)
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")  
    try:              
        dataframe=pd.read_json(r'C:\BFSI_OCR\data\statement.json')
        # print("printing dataframe" ,dataframe)
    except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")     


