import os
import settings
from api import PetFriends

pf = PetFriends()


def test_get_api_key_for_valid_user(
    email=settings.valid_email,
    password=settings.valid_password
):
    """Аутентификация пользователя с корректными полями:
    Выполняем GET-запрос на /api/key с корректными полями email и password
    Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key."""
    status, result = pf.get_api_key(email, password)

    print(status, result)

    assert status == 200
    assert 'key' in result


def test_get_api_key_for_not_valid_email_and_password(
    email=settings.not_valid_email,
    password=settings.not_valid_password
):
    """Аутентификация пользователя с некорректными полями:
    Выполняем GET-запрос на /api/key с некорректными полями email и password.
    Проверяем, что запрос API ключа возвращает статус 403 и в результате не содержится слово key."""
    status, result = pf.get_api_key(email, password)

    print(status, result)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_vacant_email_and_password(
    email=settings.vacant_email,
    password=settings.vacant_password
):
    """Аутентификация пользователя с пустыми полями:
    Выполняем GET-запрос на /api/key с пустыми полями email и password.
    Проверяем, что запрос API ключа возвращает статус 403 и в результате не содержится слово key."""
    status, result = pf.get_api_key(email, password)

    print(status, result)

    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """Получение списка всех питомцев:
    Выполняем GET-запрос на /api/pets.
    Проверяем, что запрос списка всех питомцев возвращает не пустой список."""
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    print(status, result)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_empty_key(filter=''):
    """Получение списка питомцев c пустым значением api ключа:
    Выполняем GET-запрос на /api/pets.
    Проверяем, что запрос всех питомцев возвращает статус 403."""
    status, result = pf.get_list_of_pets(settings.empty_auth_key, filter)

    print(status, result)

    assert status == 403


def test_post_add_new_pet_with_all_valid_data(
        name='Linkin Park',
        animal_type='siberian husky',
        age='1',
        pet_photo_path='images/1.jpg'
):
    """Добавление питомца cat_01 (c фото, все поля заполнены корректно):
    Выполняем POST-запрос на /api/pets.
    Проверяем, что запрос на добавление нового питомца со всеми параметрами выполняется успешно."""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    print(status, result)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_post_add_new_pet_with_vacant_data_with_foto(
    name='',
    animal_type='',
    age='',
    pet_photo_path='images/3.jpg'
):
    """Добавление питомца cat_02 (с фото, поля не заполнены):
    Выполняем POST-запрос на /api/pets.
    Проверяем, что запрос на добавление нового питомца с фото,
    но пустыми остальными параметрами, выполняется успешно."""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    print(status, result)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_put_update_pet_with_not_valid_data_without_foto(
    name='dfjhgdjdjdjdjdgjhgjyj',
    animal_type='dfjhgdjdjdjdjdgjhgjyj',
    age='dfjhgdjdjdjdjdgjhgjyj'
):
    """Изменение данных питомца cat_02 (все поля заполнены некорректно):
    Выполняем PUT-запрос на /api/pets/{pet_id} с некорректными параметрами.
    Проверяем возможность обновления информации о последнем заведенном питомце."""

    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception('There is no my pets')
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key,
        pet_id,
        name,
        animal_type,
        age
    )

    print(status, result)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_delete_last_pet():
    """Удаление добавленного питомца cat_01:
    Выполнгяем DELETE-запрос на /api/pets/{pet_id} на удаление питомца.
    Проверяем возможность удаления первого добавленного питомца."""
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        pf.add_new_pet(auth_key, 'Милашка', 'Бубльгум', "3", "images/dog_02.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    print(status)

    assert status == 200


def test_post_add_new_pet_with_not_valid_data_without_foto(
    name='!"№;%:?*',
    animal_type='!"№;%:?*',
    age='-0,1',
):
    """Добавление питомца dog_01 (без фото, все поля заполнены не корректно):
    Выполняем POST-запрос на /api/pets на добавление питомца.
    Проверяем, что запрос на добавление нового питомца без фото и некорректно заполненными полями
    выполняется успешно"""
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key,
        name,
        animal_type,
        age
    )

    print(status, result)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_put_update_pet_with_valid_data_without_foto(
    name='AC/DC',
    animal_type='great dane',
    age='2',
):
    """
    Изменение данных питомца dog_01 (без фото, все поля заполнены корректно):
    Выполнить PUT-запрос на /api/pets/{pet_id} с корректными параметрами.
    Проверяем возможность изменения данных последнего добавленного питомца"""
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key,
                                        pet_id,
                                        name,
                                        animal_type,
                                        age
    )

    print(status, result)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_post_update_pet_foto(
    pet_id='',
    pet_photo_path='images/dog_01.jpg'
):
    """Изменение данных питомца dog_01 (добавление фото):
    Выполняем POST-запрос на /api/pets/set_photo/{pet_id}
    Проверяем возможность добавление фото для последнего добавленного питомца"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(auth_key, pet_id, pet_photo_path)

    print(status, result)

    assert status == 200
    assert result['pet_photo']

def test_post_add_new_pet_with_vacant_data_without_foto(
    name='',
    animal_type='',
    age='',
):
    """Добавление питомца (без фото, поля не заполнены):
    Выполняем POST-запрос на /api/pets.
    Проверяем, что запрос на добавление нового питомца со всеми пустыми остальными параметрами выполняется успешно."""
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key,
        name,
        animal_type,
        age,
    )

    print(status, result)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_delete_last_pet():
    """Удаление добавленного питомца:
    Выполняем DELETE-запрос на /api/pets/{pet_id} на удаление питомца.
    Проверяем возможность удаления последнего добавленного питомца."""
    _, auth_key = pf.get_api_key(settings.valid_email, settings.valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        pf.add_new_pet(auth_key, 'Милашка', 'Бубльгум', "3", "images/dog_02.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    print(status)

    assert status == 200
