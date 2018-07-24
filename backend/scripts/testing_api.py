import json
import requests
import datetime

BASE_URL = "http://127.0.0.1:7999/"

ENDPOINT = "api/units/"


def create_update(d):
    r = requests.post(BASE_URL + ENDPOINT, data=d)
    # print(r.headers)
    # print(r.status_code)
    print(r)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text


data_create = {
  'unit': 1,
  'start_work': datetime.datetime.now(),
  'end_work': datetime.datetime.now(),
  'tester': 1,
  'test_object': 'Объект испытания1',
  'distance': 1,
  'note_text': 'Примечение 1',
}

create_update(data_create)