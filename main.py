import requests
import configparser
import json
from pprint import pprint
from urllib.parse import urlencode
import logging

logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w')
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

APP_ID = int(input('Введите ваш индификационный номер VK:'))

OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
params = {'client_id': APP_ID, 'redirect_uri': 'https://oauth.vk.com/blank.html', 'scope': 'photos', 'display': 'page',
          'response_type': 'token'}

OAUTH_URL = f'{OAUTH_BASE_URL}?{urlencode(params)}'
print(OAUTH_URL)


class ApiVK:

    def __init__(self, token, user_id, photo_count):
        self.token = token
        self.user_id = user_id
        self.photo_count = photo_count

    def get_photo_from_vk(self):
        param = {'access_token': self.token, 'v': '5.199', 'owner_id': self.user_id, 'album_id': 'profile', 'rev': '0',
                 'extended': '1', 'count': self.photo_count}

        response1 = requests.get('https://api.vk.com/method/photos.getAll', params=param)
        list_photo = []
        photos_dict = {}
        use_obj_name = []
        size_dict = {'size': 'z'}
        for photo in response1.json():
            #    current_photo = photo.get("items", {}).get("likes", {}).get("type")
            #    print(current_photo)
            if photo.get('items', '').get('sizes', '').get('type', '') == 'w':
                if photo.get('items', '').get('likes', '').get('count', '') in use_obj_name:
                    photo_name = photo.get('items', {}).get('likes', {}).get('count') + photo.get('items', {}).get(
                        'date')
                    photo_url = photo.get('items', {}).get('sizes', {}).get('url')

                else:
                    photo_name = photo.get('items', {}).get('likes', {}).get('count')
                    photo_url = photo.get('items', {}).get('sizes', {}).get('url')
                    use_obj_name.append(photo.get('items', {}).get('likes', {}).get('count'))

                res = requests.get(photo_url)
                with open(f'{photo_name}.jpg', 'wb') as file1:
                    file1.write(res.content)
                    photos_dict.setdefault('file_name', f"{photo_name}.jpg")
                    photos_dict.update(size_dict)
                    list_photo.append(photos_dict)
        return list_photo


class YDisk:

    def __init__(self, tokenyd, list_photo, url_folder_create, url_get_link, url_for_upload):
        self.tokenyd = tokenyd
        self.list_foto = list_photo
        self.url_folder_create = url_folder_create
        self.url_get_link = url_get_link
        self.url_for_upload = url_for_upload

    def Folder_create(self, tokenyd):
        self.url_folder_create = 'https://cloud-api.yandex.net/v1/disk/resourse'
        params_dict = {'path': 'image'}
        headers_dict2 = {'Authorization': tokenyd}
        response2 = requests.put(self.url_folder_create, params=params_dict, headers=headers_dict2)
        return response2.status_code

    def create_url(self, tokenyd):
        self.url_get_link = 'https://cloud-api.yandex.net/v1/disk/resourse/upload'
        params_dict = {'path': 'image/photos.jpg'}
        headers_dict3 = {'Authorization': tokenyd}
        response3 = requests.get(self.url_get_link, params=params_dict, headers=headers_dict3)
        url_for_upload = response3.json().get('href')
        return url_for_upload


with open('foto.json', 'w') as f:
    json.dump(list_photo, f)
with open('foto.json', 'rb') as file:
    config = configparser.ConfigParser()
    config.read('settings.ini')

    TOKENYD = config['token']['tokenyd']
    headers_dict = {'Authorization': TOKENYD}
    response = requests.put('url_for_upload', files={'file': file}, headers=headers_dict)
    print(response.status_code)


if __name__ == 'main':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    TOKENVK = config['token']['tokenvk']
    vk_client = (ApiVK(TOKENVK, 838612895, 5))
    photos_info = vk_client.get_photo_from_vk()
    pprint(photos_info)
