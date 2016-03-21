import requests
import json
host = 'http://localhost:8000'

def print_response(response):
    print(response.status_code)
    print(response.content)
    print(response.headers)
    print(response.url)


def generic_get(path, data=None):
    url = host + path
    response = requests.get(url, data=data)
    print_response(response)

def generic_delete(path):
    url = host + path
    response = requests.delete(url)
    print_response(response)


def create_asset():
    path = '/asset'
    url = host + path
    payload = {'title': 'apple',
               'description': 'apple',
               'thumbnail_url': 'apple',}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)
    response = requests.post(url, data=data, headers=headers)
    #response = requests.post(url, data=data)
    print_response(response)

def get_asset():
    path = '/asset/1'
    generic_get(path)

def put_asset():
    path = '/asset/10'
    url = host + path
    payload = {'title': 'aabb',
               'description': 'aabb',}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)
    response = requests.put(url, data=data, headers=headers)
    #response = requests.post(url, data=data)
    print_response(response)


def delete_asset():
    path = '/asset/15'
    generic_delete(path)

def get_assets():
    path = '/asset/'
    data = {'number': 3, 'sort': 'standard'}
    #data = None
    generic_get(path, data=data)

def create_credit():
    path = '/credit'
    url = host + path
    payload = {'job_type': 'director',
               'name': 'woooo',}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)
    response = requests.post(url, data=data, headers=headers)
    print_response(response)

def create_asset_credit():
    path = '/asset/2/credit/3'
    url = host + path
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    print_response(response)

def list_asset_credits():
    path = '/asset/1/credits'
    generic_get(path)

def list_credit_assets():
    path = '/credit/3/assets'
    generic_get(path)

def put_credit():
    path = '/credit/23'
    url = host + path
    payload = {'job_type': 'director',
               'name': 'cool',}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)
    response = requests.put(url, data=data, headers=headers)
    print_response(response)


def delete_credit():
    path = '/credit/16'
    generic_delete(path)

def get_credit():
    path = '/credit/23'
    generic_get(path)




#create_assset()
#get_asset()
#get_assets()
# for i in range(6):
#     create_credit()
# delete_credit()
# put_credit()
# get_credit()
#delete_asset()
# put_asset()
# get_assets()

#create_asset()
create_credit()
#create_credit()
#create_asset_credit()
#list_asset_credits()
list_credit_assets()
