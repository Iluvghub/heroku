import re
import base64
import requests
from urllib.parse import urlparse, parse_qs

CRYPT = "d1AwOEI1Wmc3NVQrbitMWTZjakVra2xJYmFadURpM09rTzQyTHQ0MDBHVT0%3D"
url = input('enter url:') 

def gdtot(url: str) -> str:
    """ Gdtot google drive link generator
    By https://github.com/xcscxr """

    
    match = re.findall(r'https?://(.+)\.gdtot\.(.+)\/\S+\/\S+', url)[0]

    with requests.Session() as client:
        client.cookies.update({'crypt': CRYPT})
        res = client.get(url)
        res = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
    matches = re.findall('gd=(.*?)&', res.text)
    try:
        decoded_id = b64decode(str(matches[0])).decode('utf-8')
    except:
        raise DirectDownloadLinkException("ERROR: Try in your broswer, mostly file not found or user limit exceeded!")
    return f'https://drive.google.com/open?id={decoded_id}'
print(gdtot(url)) 
