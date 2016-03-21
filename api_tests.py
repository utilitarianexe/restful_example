import requests
import json
host = 'http://localhost:8000'

def print_response(response):
    print(response.status_code)
    str_response = response.content.decode('utf-8')
    response_json = json.loads(str_response)
    print(response_json)
    print(response.headers)
    print(response.url)

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def remove_keys(obj, keys):
    if isinstance(obj, dict):
        for key in keys:
            del obj[key]
        return obj
    elif isinstance(obj, list):
        for item in obj:
            remove_keys(item, keys)
        return obj
    else:
        return obj


def check_response(response, status_code,
                   expected_content=None,
                   keys_to_ignore=None):
    assert response.status_code == status_code
    if expected_content is not None:
        str_response = response.content.decode('utf-8')
        response_json = json.loads(str_response)
        if keys_to_ignore is not None:
            response_json = remove_keys(response_json, keys_to_ignore)
        print(response_json, expected_content)
        assert ordered(response_json) == ordered(expected_content)


def generic_get(path, data=None):
    url = host + path
    response = requests.get(url, data=data)
    print_response(response)

def generic_delete(path):
    url = host + path
    response = requests.delete(url)
    print_response(response)


def create_asset(payload):
    path = '/asset'
    url = host + path
    data = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    #response = requests.post(url, data=data)
    print_response(response)
    return response

def create_example_asset():
    create_asset({'title': 'apple',
                  'description': 'apple',
                  'thumbnail_url': 'apple',},)

def create_assets_test():
    payloads = [{'title': 'apple',
                 'description': 'apple',
                 'thumbnail_url': 'apple',},
                {'title': 'peter',
                 'description': 'peter',
                 'thumbnail_url': 'apple',},
                {'title': 'bannana',
                 'description': 'apple',
                 'thumbnail_url': 'apple',},
                {'title': 'orange',
                 'description': 'apple',
                 'thumbnail_url': 'apple',},
                {'title': 'carrot',
                 'description': 'apple',
                 'thumbnail_url': 'apple',},]
    for payload in payloads:
        response = create_asset(payload)
        check_response(response, 201,
                       expected_content=payload,
                       keys_to_ignore=['creation_date'])

    return response.headers['location']

def update_existing_asset_test(asset_location):
    payload = {'title': 'aabb'}
    headers = {'Content-Type': 'application/json'}
    expected_content = {'title': 'aabb',
                        'description': 'apple',
                        'thumbnail_url': 'apple',}
    data = json.dumps(payload)
    response = requests.put(asset_location, data=data, headers=headers)
    check_response(response, 200,
                   expected_content=expected_content,
                   keys_to_ignore=['creation_date'])


def get_asset_test(asset_location):
    expected_content = {'title': 'aabb',
                        'description': 'apple',
                        'thumbnail_url': 'apple',}
    response = requests.put(asset_location)
    check_response(response, 200,
                   expected_content=expected_content,
                   keys_to_ignore=['creation_date'])

def delete_asset_test(asset_location):
    pass


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


def test_api():
    example_asset_location = create_assets_test()
    update_existing_asset_test(example_asset_location)
    get_asset_test(example_asset_location)
    delete_asset_test(example_asset_location)
    get_asssets_tests()

test_api()

