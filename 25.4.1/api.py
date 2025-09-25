import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

def get_code_json_or_text(response):
    result = ''
    try:
        result = response.json()
    except json.decoder.JSONDecodeError:
        result = response.text
    return response.status_code, result


class PetFriends:
    """API-библиотека к веб приложению Pet Friends"""

    BASE_URL = 'https://petfriends.skillfactory.ru/'
    ALL_PETS = ''
    MY_PETS = 'my_pets'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API и возвращает статус запроса и результат в формате JSON
        с уникальным ключом пользователя"""

        headers = {
            'email': email,
            'password': password,
        }
        return get_code_json_or_text(requests.get(
            self.BASE_URL + 'api/key',
            headers=headers))

    def get_list_of_pets(self, auth_key: json,
                         all_or_my_pets: str = '') -> json:
        """Метод делает запрос к API сервера и возвращает
        статус запроса и результат в формате JSON со списком
        наденных питомцев, совпадающих с фильтром."""

        headers = {'auth_key': auth_key['key']}
        all_or_my_pets = {'filter': all_or_my_pets}

        return get_code_json_or_text(requests.get(
            self.BASE_URL + 'api/pets',
            headers=headers,
            params=all_or_my_pets))

    def add_new_pet(self, auth_key: json,
                    name: str,
                    animal_type: str,
                    age: str,
                    pet_photo_path: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и
        возвращает статус запроса на сервер и результат в формате JSON
        с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (
                    pet_photo_path,
                    open(pet_photo_path, 'rb'), 'image/jpeg'
                )
            })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        return get_code_json_or_text(requests.post(
            self.BASE_URL + 'api/pets',
            headers=headers,
            data=data))

    def delete_pet(self, auth_key: json,
                   pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца
        по указанному ID и возвращает статус запроса и результат в формате JSON
        с текстом уведомления о успешном удалении."""

        headers = {'auth_key': auth_key['key']}

        return get_code_json_or_text(requests.delete(
            self.BASE_URL + 'api/pets/' + pet_id,
            headers=headers))

    def update_pet_info(self,
                        auth_key: json,
                        pet_id: str,
                        name: str,
                        animal_type: str,
                        age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомца
        по указанному ID и возвращает статус запроса и result в формате JSON
        с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        return get_code_json_or_text(requests.put(
            self.BASE_URL + 'api/pets/' + pet_id,
            headers=headers,
            data=data))

    def add_new_pet_without_photo(self,
                                  auth_key: json,
                                  name: str,
                                  animal_type: str,
                                  age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце
        без фото и возвращает статус запроса на сервер и результат
        в формате JSON с данными добавленного питомца.
        Здесь отрабатывается POST API запрос."""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        return get_code_json_or_text(requests.post(
            self.BASE_URL + 'api/create_pet_simple',
            headers=headers,
            data=data))

    def add_foto_of_pet(self,
                        auth_key: json,
                        pet_id: str,
                        pet_photo_path: str) -> json:
        """Метод отправляет запрос на сервер на добавление данных питомца
        - фото - по указанному ID и возвращает статус запроса и result в формате JSON
        с обновлённыи данными питомца.
        Здесь отрабатывается POST API запрос."""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo_path,
                                  open(pet_photo_path, 'rb'),
                                  'image/jpeg')})
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        return get_code_json_or_text(requests.post(
            self.BASE_URL + 'api/pets/set_photo/' + pet_id,
            headers=headers,
            data=data))
