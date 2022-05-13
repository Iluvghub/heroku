import re
import requests
from lxml import etree
from urllib.parse import urlparse

EMAIL = "Johnwick.mirror.leech@gmail.com"
PWSSD = "Modapps@430"
GDRIVE_FOLDER_ID = "1WuaaTESEiOFAvdjS0JDFReNZKR2hjTgc"
url = input('enter url:') 

def appdrive_dl(url: str) -> str:

 
     

    account = {'email': EMAIL, 'passwd': PWSSD}

    client = requests.Session()

    client.headers.update({

        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"

    })

    data = {

        'email': account['email'],

        'password': account['passwd']

    }

    client.post(f'https://{urlparse(url).netloc}/login', data=data)

    data = {

        'root_drive': '',

        'folder': GDRIVE_FOLDER_ID

    }

    client.post(f'https://{urlparse(url).netloc}/account', data=data)

    res = client.get(url)

    key = re.findall('"key",\s+"(.*?)"', res.text)[0]

    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")

    info = re.findall('>(.*?)<\/li>', res.text)

    info_parsed = {}

    for item in info:

        kv = [s.strip() for s in item.split(':', maxsplit = 1)]

        info_parsed[kv[0].lower()] = kv[1] 

    info_parsed = info_parsed

    info_parsed['error'] = False

    info_parsed['link_type'] = 'login' # direct/login

    headers = {

        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",

    }

    data = {

        'type': 1,

        'key': key,

        'action': 'original'

    }

    if len(ddl_btn):

        info_parsed['link_type'] = 'direct'

        data['action'] = 'direct'

    while data['type'] <= 3:

        boundary=f'{"-"*6}_'

        data_string = ''

        for item in data:

             data_string += f'{boundary}\r\n'

             data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'

        data_string += f'{boundary}--\r\n'

        gen_payload = data_string

        try:

            response = client.post(url, data=gen_payload, headers=headers).json()

            break

        except: data['type'] += 1

    if 'url' in response:

        info_parsed['gdrive_link'] = response['url']

    elif 'error' in response and response['error']:

        info_parsed['error'] = True

        info_parsed['error_message'] = response['message']

    else:

        info_parsed['error'] = True

        info_parsed['error_message'] = 'Something went wrong :('

    if info_parsed['error']: return info_parsed

    if urlparse(url).netloc == 'driveapp.in' and not info_parsed['error']:

        res = client.get(info_parsed['gdrive_link'])

        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]

        info_parsed['gdrive_link'] = drive_link

    info_parsed['src_url'] = url

    if info_parsed['error']:

        raise DirectDownloadLinkException(f"{info_parsed['error_message']}")

    return info_parsed["gdrive_link"]
   
print(appdrive_dl(url))   
