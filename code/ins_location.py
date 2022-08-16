from instascrape import Location
from instascrape import Post
import logging
from urllib.parse import urlparse
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook, Workbook
import time
from random import randrange

SET_URL_PATH = "./log/268647134.log (the log file name created in step one)"
SESSION_ID = "this can be found when you log in "

USER_POST_LINKS = []
DATA = []
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid="+SESSION_ID+";"
}
filename = SET_URL_PATH.split('/')[-1:][0].split('.')[0]
Path("./datanew").mkdir(parents=True, exist_ok=True)
Path(f"./datanew/img_{filename}").mkdir(parents=True, exist_ok=True)

with open(SET_URL_PATH) as f:
    listNew = list(f)
for item in listNew:
    if "https://www.instagram.com/p/" in item:
        url = (urlparse(item).path).rpartition('- ')[2]
        if url not in USER_POST_LINKS:
            USER_POST_LINKS.append(url)

df_parse_log = pd.DataFrame(USER_POST_LINKS, columns= ['URL'])
df_parse_log.to_json(r'./datanew/'+filename+"_urls"+'.json', orient='index', indent=2)

# for item in USER_POST_LINKS[0:100, 100:200, 200:300......]: 
for item in USER_POST_LINKS[20300:20400]: 
    try:
        user_post = Post(item)
        user_post.scrape(headers=headers)
        print(user_post.to_dict())
        DATA.append(user_post.to_dict())
        try:
            # user_post.download(f"./data/img_{filename}/{user_post.username}_{user_post.upload_date}.png")
            user_post.download(f"./datanew/img_{filename}/{USER_POST_LINKS.index(item)}_{user_post.shortcode}.png")
        except:
            print("Failed to download: ", item)
    except:
        print("Failed: ", item)
    time.sleep(randrange(7))

df = pd.DataFrame(DATA)
df.to_excel(r'./foldername/'+filename+'_data'+'.xlsx', index = False, header=True)
