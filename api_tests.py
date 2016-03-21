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
    try:
        assert response.status_code == status_code
    except AssertionError:
        print('failed test did not get expected status code', response.status_code, status_code)
    if expected_content is not None:
        str_response = response.content.decode('utf-8')
        response_json = json.loads(str_response)
        if keys_to_ignore is not None:
            response_json = remove_keys(response_json, keys_to_ignore)
        try:
            assert ordered(response_json) == ordered(expected_content)
        except AssertionError:
            print('failed test did not get expected content', response_json, expected_content)


def generic_get(path, data=None):
    url = host + path
    response = requests.get(url, data=data)
    return response


def generic_delete(path):
    url = host + path
    response = requests.delete(url)

def create_asset(payload):
    path = '/assets'
    url = host + path
    data = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    #response = requests.post(url, data=data)
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
    locations = []
    for payload in payloads:
        response = create_asset(payload)
        locations.append(response.headers['location'])
        check_response(response, 201,
                       expected_content=payload,
                       keys_to_ignore=['creation_date'])

    return locations

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
    response = requests.delete(asset_location)
    check_response(response, 204)

def get_assets_tests():
    expected_content = [{'title': 'apple',
                         'description': 'apple',
                         'thumbnail_url': 'apple',},
                        {'title': 'bannana',
                         'description': 'apple',
                         'thumbnail_url': 'apple',},
                        {'title': 'orange',
                         'description': 'apple',
                         'thumbnail_url': 'apple',},
                        {'title': 'peter',
                         'description': 'peter',
                         'thumbnail_url': 'apple',},
                    ]

    path = '/assets'
    data = {}
    response = generic_get(path, data=data)
    check_response(response, 200, expected_content=expected_content,
                   keys_to_ignore=['creation_date'])
    
    data = {'sort': 'reverse'}
    expected_content = list(reversed(expected_content))
    response = generic_get(path, data=data)
    check_response(response, 200, expected_content=expected_content,
                   keys_to_ignore=['creation_date'])

    data = {'sort': 'standard', 'number': 3}
    expected_content = list(reversed(expected_content))[:3]
    response = generic_get(path, data=data)
    check_response(response, 200, expected_content=expected_content,
                   keys_to_ignore=['creation_date'])


def create_credit(payload):
    path = '/credits'
    url = host + path
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)
    response = requests.post(url, data=data, headers=headers)
    return response


def create_credits_test():
    payloads = [{'name': 'wheat',
                 'job_type': 'apple', },
                {'name': 'rye',
                 'job_type': 'apple', },
                {'name': 'corn',
                 'job_type': 'apple', },
                {'name': 'hay',
                 'job_type': 'apple', },]
    locations = []
    for payload in payloads:
        response = create_credit(payload)
        check_response(response, 201,
                       expected_content=payload,)
        locations.append(response.headers['location'])

    return locations

def update_existing_credit_test(credit_location):
    payload = {'name': 'oats'}
    headers = {'Content-Type': 'application/json'}
    expected_content = {'name': 'oats',
                        'job_type': 'apple', }
    data = json.dumps(payload)
    response = requests.put(credit_location, data=data, headers=headers)
    check_response(response, 200,
                   expected_content=expected_content,)


def get_credit_test(credit_location):
    expected_content = {'name': 'oats',
                        'job_type': 'apple',}
    response = requests.put(credit_location)
    check_response(response, 200,
                   expected_content=expected_content,)

def delete_credit_test(credit_location):
    response = requests.delete(credit_location)
    check_response(response, 204)


def create_asset_credit_test(asset_location, credit_location):
    asset_id = asset_location[asset_location.rfind('/') + 1:]
    credit_id = credit_location[credit_location.rfind('/') + 1:]
    path = '/assets/{}/credits/{}'.format(asset_id, credit_id)
    url = host + path
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    check_response(response, 201)

def assets_credits_test(location):
    expected_content = [{'name': 'wheat',
                         'job_type': 'apple', },
                        {'name': 'rye',
                         'job_type': 'apple', },]
    url = location + '/credits'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    check_response(response, 200, expected_content=expected_content)

def credits_assets_test(location):
    expected_content = [{'title': 'apple',
                         'description': 'apple',
                         'thumbnail_url': 'apple',},
                        {'title': 'peter',
                         'description': 'peter',
                         'thumbnail_url': 'apple',},]
    url = location + '/assets'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    check_response(response, 200,
                   expected_content=expected_content,
                   keys_to_ignore=['creation_date'])

def list_asset_credits(location):
    path = location + '/credits'
    generic_get(path)

def list_credit_assets():
    path = '/credit/3/assets'
    generic_get(path)


def test_api():
    example_asset_locations = create_assets_test()
    update_existing_asset_test(example_asset_locations[-1])
    get_asset_test(example_asset_locations[-1])
    delete_asset_test(example_asset_locations[-1])
    get_assets_tests()

    example_credit_locations = create_credits_test()
    update_existing_credit_test(example_credit_locations[-1])
    get_credit_test(example_credit_locations[-1])
    delete_credit_test(example_credit_locations[-1])
    create_asset_credit_test(example_asset_locations[0], example_credit_locations[0])
    create_asset_credit_test(example_asset_locations[0], example_credit_locations[1])
    create_asset_credit_test(example_asset_locations[1], example_credit_locations[0])
    assets_credits_test(example_asset_locations[0])
    credits_assets_test(example_credit_locations[0])

test_api()

