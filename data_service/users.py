#!/usr/bin/env python

#-----------------------------------------------------------------------
# users.py
#-----------------------------------------------------------------------

import hashlib
import random
import requests
import json
from base64 import b64encode, b64decode
from datetime import datetime
from os import path

def generateHeaders():
    created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32)])
    nonce_bytes = b64encode(bytes(nonce, 'ascii')).decode()

    username = 'zbatscha'
    password = '4d8a6a21c08ee526829032f02e06884a'    # use your own from /getkey
    password_digest = (nonce + created + password).encode('ascii')
    generated_digest = b64encode(hashlib.sha256(password_digest).digest()).decode()
    headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': f'UsernameToken Username="{username}", PasswordDigest="{generated_digest}", Nonce="{nonce_bytes}", Created="{created}"'
    }
    return headers

def getUndergraduate(netid):
    url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates'
    url = path.join(url, netid)
    headers = generateHeaders()
    try:
        response = requests.get(
            url=url,
            headers=headers)
        response.raise_for_status()
        undergrad = json.loads(response.content)
        return undergrad
    except requests.exceptions.HTTPError as err:
        print(err)
        return None

if __name__=="__main__":

    undergrad = getUndergraduate('cl43')
    print(undergrad)
