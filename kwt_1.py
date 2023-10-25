import requests
import pandas as pd
import os
import json
import logging
from tqdm import tqdm
import time

output = "C:/Store_Migration/Loyalty_output"

if not os.path.exists(output):
    os.makedirs(output)
    print('Creating folder: ', output)
    print('===============================================')
else:
    os.makedirs(output, exist_ok=True)
    print('Output folder already exists ', output)
    print('===============================================')

file = r"C:\Store_Migration/\Splits_output\kwt_1.csv"


cols = ['fname', 'lname', 'email', 'mobile1']
df = pd.read_csv(file, encoding="UTF-8-SIG")
df = df.astype(str)


df['fname'] = df['fname'].fillna('')
df['lname'] = df['lname'].fillna('')
df = df.fillna(value='')

df['mobile1'] = df['mobile'].astype(str).apply(lambda x: '+' + x)
df['email'] = df['email'].apply(lambda x: x.lower())


status = []

logger = logging.getLogger('migration_logger')
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler(os.path.join(output, 'kwt_1_error_log.json'))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

with tqdm(total=len(df), desc='Progress') as pbar:
    for _, row in df.iterrows():
        try:
            payload = json.dumps({
                "customer": {
                    "first_name": row['fname'],
                    "last_name": row['lname'],
                    "email": row['email'],
                    "phone": row['mobile1'].split('.')[0],
                    "verified_email": True,
                    "password": "#a12345!",
                    "password_confirmation": "#a12345!",
                    "send_email_welcome": False,
                    "multipass_identifier": row['email'],
                    "tags": "RTLoyalty"
                }
            })

            url = "https://{YourStoreName}.myshopify.com/admin/api/2023-01/customers.json" # Change the StoreName With your Own

            headers = {
                'X-Shopify-Access-Token': '{Put Your Access Token Here}', # Change Access Token With Your Own
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            status.append(response.status_code)
        except Exception as e:
            logger.error(f"Error creating customer: {e}")

        pbar.update(1)
        time.sleep(0.01)

logger.removeHandler(file_handler)
file_handler.close()


