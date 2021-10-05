from django.shortcuts import render
from requests.api import request

def home(request):
    return render(request,'content/index.html',{})

####################################################

from django.shortcuts import render
from decouple import config
import base64
import requests
from content import decode_jwt
import os

def home(request):
    context = {}
    try:
        code = request.GET.get('code')
        userData = getTokens(code)
        context['name'] = userData['name']
        context['status'] = 1
        

        response = render(request, 'content/index.html', context)
        response.set_cookie('sessiontoken', userData['id_token'])
        return response, print("status 111111111111111111111111111111111111111111111111111111111111111111111111111111")
    except:
        token = getSession(request)
        if token is not None:
            userData = decode_jwt.lambda_handler(token, None)
            context['name'] = userData['name']
            context['status'] = 1
            return render(request, 'content/index.html', context)
        return render(request, 'content/index.html', {'status': 0}, print("000000000000000000000000000000000000000000000000000000000000000000000000000000000000"))

def getTokens(code):
    TOKEN_ENDPOINT = config('TOKEN_ENDPOINT')
    REDIRECT_URI = config('REDIRECT_URI')
    CLIENT_ID = config('CLIENT_ID')
    CLIENT_SECRET = config('CLIENT_SECRT')

    encodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO-8859-1")).decode("ascii")

    headers = {
        'Content-Type': 'application/x-www-from-urlencoded',
        'Authorization': f'Basic{encodeData}'
    }

    body = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(TOKEN_ENDPOINT, data=body, headers=headers)
    
    id_token = response.json()['id_token']

    userData = decode_jwt.lambda_handler(id_token, None)

    if not userData:
        return False
    
    user = {
        'id_token': id_token,
        'name': userData['name'],
        'emai': userData['email'],
    }
    return user
    
def getSession(request):
    try:
        response = request.COOKIES["sessiontoken"]
        return response
    except:
        return None
print("8888888888888888888888888888888888")
print(requests.request.COOKIES["sessiontoken"])


#########################################################################
