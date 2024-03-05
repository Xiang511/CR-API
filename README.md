# Clash-Royale-API
![GitHub last commit](https://img.shields.io/github/last-commit/Xiang511/CR-API?display_timestamp=author&style=for-the-badge&color=blue)
![Github Created At](https://img.shields.io/github/created-at/Xiang511/CR-API?style=for-the-badge&color=blue)
![GitHub Release](https://img.shields.io/github/v/release/Xiang511/CR-API?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/Xiang511/CR-API?style=for-the-badge&color=blue)

Accessing the CR-API using Python 

Users must obtain the corresponding API key to use. Please go to [Official Document](https://developer.clashroyale.com/#/)  

### Features 
-  Search Clan information
-  Search Player information  
-  Search local rankings 
-  Search player achievement records

### Under development
- Implement a GUI

## Example Usage
Here are some example code samples.

DEMO : [https://www.youtube.com/watch?v=BKnR_kre6QI&ab_channel=XiangFang](https://www.youtube.com/watch?v=BKnR_kre6QI&ab_channel=XiangFang)
### FindClan.py

> Search Clan information


```python
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
```
