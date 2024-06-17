import requests
import pandas as pd
import time

#Calculate starting time
start_time = time.time()

# Enter your key
# Go to https://developer.clashroyale.com/#/ 

API_KEY = ""
headers = {
    "Authorization": "Bearer {}".format(API_KEY)
}

# GET ClanTag
#ex: %23QCRY22P8

clan_tag = "%23QCRY22P8"


url = "https://api.clashroyale.com/v1/clans/{}".format(clan_tag)
response = requests.get(url, headers=headers)


try:
    if response.status_code == 200:
        clan = response.json()

        df = pd.DataFrame(clan["memberList"])
        df.to_excel("FindClan.xlsx")

        
        end_time = time.time()
        
        print(f"Time：{end_time - start_time}")
    else:
        print(response.status_code)
except Exception as e:
    print(e)