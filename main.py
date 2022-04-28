# Made By Leho | leho.dev | github.com/lehoooo
import datetime
import json
from bs4 import *
import requests
import threading
import time

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        webhook_url = config['webhook_url']
        role_id = config['role_id']
        delay = config['delay']
except:
    print('config.json not found or error loading')
    exit(1)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

params = {
    'th': '1',
}

links_read = open("links.txt", "r")
links = links_read.readlines()
links_read.close()

def check_stock(url):
    while True:
        response = requests.get(str(url), params=params, headers=headers)
        if response.status_code == 200:
            if "In stock." in response.text:
                print("In stock: " + str(url))
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('span', {'id': 'productTitle'}).text
                print(title)
                # send webhook to discord
                sendwebhook(str(title), str(url))
                print("Waiting...")
                time.sleep(delay * 60)

            else:
                print("Out of stock: " + str(url))
                print("Waiting...")
                time.sleep(delay * 60)


def sendwebhook(title, itemurl):
    x = datetime.datetime.now()
    timenow = x.strftime("%x %X")
    webhook_content = {
      "content": "<@&" + str(role_id) + ">",
      "embeds": [
        {
          "title": "IN STOCK",
          "description": str(title),
          "color": 5439232,
          "fields": [
            {
              "name": "Time",
              "value": str(timenow),
            }
          ],
          "footer": {
            "text": "Amazon Notifier | Made With 💖 By Leho"
          }
        },
        {
          "title": "CLICK HERE TO ORDER",
          "url": str(itemurl),
          "color": 11337983,
        "footer": {
            "text": "Amazon Notifier | Made With 💖 By Leho"
          }
        }
      ],
      "attachments": []
    }
    r = requests.post(webhook_url, data=json.dumps(webhook_content), headers={'Content-Type': 'application/json'})
    print(r.text)
    print(r.status_code)


for x in range(len(links)):
    print("queuing link " + str(links[x]))
    thread = threading.Thread(target=check_stock, args=(links[x],)).start()
print("finished threading")
