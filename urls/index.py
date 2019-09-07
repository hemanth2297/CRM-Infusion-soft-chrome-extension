
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from infusionsoft.client import Client
from django.core.cache import cache
from time import time
import requests

client_id = "kf5pjr48ukm4fzemgqcc7f62"
client_secret = "wVfzTj3a55"
redirect_url="http://127.0.0.1:8210/code/"
client = Client(client_id, client_secret,None)
# client.set_token("zcmk3enshrgwvdhmewarehpe")
# client.end_of_life=1000000000000000


if(cache.get("InfusionSoft_ClientKey")):
    client.set_token(cache.get("InfusionSoft_ClientKey"))
    client.end_of_life = cache.get("InfusionSoft_ClientEndTime")

def is_expired():
    return client.end_of_life >int(time())


def auth(request):
    if(client.token and is_expired()):
        return render(request, 'auth.html')
    else:
        return render(request, 'index.html')

@csrf_exempt
def onClickAuthenticate(request):

    url = client.oauth_access(redirect_url)
    return redirect(url)

@csrf_exempt
def get_Code(request):
    if (client.token and is_expired()):
        return render(request, 'auth.html')

    try :

        code=request.GET.get('code')
        token = client.exchange_code(redirect_url,code)
        client.set_token(token["access_token"])
        client.expires_in = token["expires_in"]
        client.end_of_life = int(time()) + client.expires_in

        cache.set('InfusionSoft_ClientKey',client.token)
        cache.set('InfusionSoft_ClientEndTime',client.end_of_life)
    except:
        return render(request, 'index.html')

    return render(request, 'auth.html')

@csrf_exempt
def get_Contact(request):
    email = request.POST.get('email', False)
    params={"email": email}
    url = '{0}{1}'.format(client.api_base_url, "contacts")

    client.header["Authorization"] = "Bearer " + client.token
    response = requests.request("get", url, headers=client.header, params=params)
    output="Contact Not Found"
    if(client.parse_response(response)["count"]>0):
        output="Contact Found"

    content={
        'output': output
    }
    return render(request, 'auth.html',content)


@csrf_exempt
def add_Contact(request):

    name = request.POST.get('name', False)
    email = request.POST.get('email', False)

    data = {'email_addresses': [{'email': email, 'field': 'EMAIL1'}], 'given_name': name}
    create_contact = client.create_contact(**data)
    if(create_contact):
        content = {
            'output': "Contact is created Successfully"
        }
    return render(request, 'auth.html',content)



