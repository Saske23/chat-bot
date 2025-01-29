import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import wikipedia
import requests
import math
import random


token = ...
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
phrase_else = ['Я тебя не понел.', 'А это к чему?', 'Я еще так не умею.'] # фраза если человек написал что-то непонятное и не подходит не под одну функцию
pharse_howareyou = ['У меня всегда отлично.', 'Да вот новости читаю', 'Как всегда хорошо'] # фраза если человек написал 'как дела' или 'как дела?'


def write_message(user_id, message): # функция чат-бота, чтобы писать челевеку томуже, который писал
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 100000)})


def info_city(user_id, cities): # функция, выводящая информацию по городу(страна, регион, в котором находится город, координаты)
    for city in cities:
        geo_reqest = 'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=' + city + '&format=json'
        response = requests.get(geo_reqest)
        if not response:
            write_message(user_id, 'Город не найден')
        json_response = response.json()
        toponym_country = (json_response['response']['GeoObjectCollection']['featureMember'][0]
                    ['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName'])
        toponym_district = (json_response["response"]["GeoObjectCollection"]["featureMember"][0]
                            ["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][1]["name"])
#       toponym_region = (json_response["response"]["GeoObjectCollection"]["featureMember"][0]
#                         ["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][2]["name"])
        toponym_coordinates = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        write_message(user_id, 'Страна - ' + toponym_country)
        write_message(user_id, 'Округ - ' + toponym_district)
        write_message(user_id, 'Координаты - ' + toponym_coordinates)


def info_postal(user_id, address): # функция, выводящая почтовый индекс по адресу
    response = requests.get("http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + address + "&format=json")
    if not response:
        write_message(user_id, 'Адрес не найден')
        
    response = response.json()
    postal_code = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
    write_message(user_id, 'Почтовый индекс ' + postal_code)


def info_wiki(user_id, wiki_search): # функция, выводящая информацию из wikipedia
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + wiki_search + "&format=json")
    if not response:
        write_message(user_id, 'Адрес не найден')
    
    response = response.json()
    title_0 = response["query"]["search"][0]["title"]
    info_0 = response["query"]["search"][0]["snippet"]

    title_1 = response["query"]["search"][1]["title"]
    info_1 = response["query"]["search"][1]["snippet"]

    title_2 = response["query"]["search"][2]["title"]
    info_2 = response["query"]["search"][2]["snippet"]

    title_3 = response["query"]["search"][3]["title"]
    info_3 = response["query"]["search"][3]["snippet"]

    title_4 = response["query"]["search"][4]["title"]
    info_4 = response["query"]["search"][4]["snippet"]

    title_5 = response["query"]["search"][5]["title"]
    info_5 = response["query"]["search"][5]["snippet"]
    write_message(user_id, title_0)
    write_message(user_id, info_0)
    write_message(user_id, title_1) 
    write_message(user_id, info_1)
    write_message(user_id, title_2) 
    write_message(user_id, info_2)
    write_message(user_id, title_3)
    write_message(user_id, info_3)
    write_message(user_id, title_4) 
    write_message(user_id, info_4)
    write_message(user_id, title_5) 
    write_message(user_id, info_5)


def get_distance(user_id, city_name_1, city_name_2): # функция, выводящая расстояние между городами
    geo_reqest = 'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=' + city_name_1 + '&format=json'
    response = requests.get(geo_reqest)
    if not response:
        write_message(user_id, 'Город не найден')
    json_response = response.json()
    pos1 = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]

    geo_reqest = 'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=' + city_name_2 + '&format=json'
    response = requests.get(geo_reqest)
    json_response = response.json()
    pos2 = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    
    p1_1 = pos1.split(' ')[0]
    p1_2 = pos1.split(' ')[1]
    p2_1 = pos2.split(' ')[0]
    p2_2 = pos2.split(' ')[1]
    p1 = (float(p1_1), float(p1_2))
    p2 = (float(p2_1), float(p2_2))
    
    radius = 6373.0
    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)
    distance = radius * c

    write_message(user_id, str(distance) + ' км')


def main(): # центральная функция, отвечающая за преобразование текста и вызов других функций
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()

                if request == 'привет':
                    write_message(event.user_id, 'Привет, привет')
                elif '.' in request:
                    write_message(event.user_id, 'Пишите без точек, хоть это и не грамотно:)')
                elif request == 'функции' or request == 'твои функции':
                    write_message(event.user_id, '1)Информация о городе: страна, округ и координаты(нужно ввести "информация_о_городе ...(название города)")')
                    write_message(event.user_id, '2)Информация по адрессу, его постал индекс(нужно ввести "информация_по_адресу ...(адресс)")')
                    write_message(event.user_id, '3)Информация из википедии(нужно ввести "информация_википедии ...(то что ищешь)")')
                    write_message(event.user_id, '4)Расстояние между городами(нужно ввести "расстояние_между...(первый город пробел второй город)")')
                elif request.split(' ')[0].lower() == 'информация_о_городе' or request.split(' ')[0].lower() == 'инфа_о_городе':
                    cities = request.split(' ')[1].lower()
                    if (cities != ' ' or cities != '') and request.split(' ')[2] != '':
                        info_city(event.user_id, cities)
                    else:
                        write_message(event.user_id, 'Вы ввели что-то не верно')
                elif request.split(' ')[0].lower() == 'информация_по_адресу' or request.split(' ')[0].lower() == 'инфа_по_адресу':
                    address = request.split(' ')[1].lower()
                    if (address != ' ' or address != '') and request.split(' ')[2] != '':
                        info_postal(event.user_id, address)
                    else:
                        write_message(event.user_id, 'Вы ввели что-то не верно')
                elif request.split(' ')[0].lower() == 'информация_википедии' or request.split(' ')[0].lower() == 'инфа_википедии':
                    wiki_search = request.split(' ')[1].lower()
                    if (wiki_search != ' ' or wiki_search != '') and request.split(' ')[2] != '':
                        info_wiki(event.user_id, wiki_search)
                    else:
                        write_message(event.user_id, 'Вы ввели что-то не верно')
                elif request.split(' ')[0].lower() == 'расстояние_между':
                    city_name_1 = request.split(' ')[1].lower()
                    city_name_2 = request.split(' ')[2].lower()
                    if (city_name_1 != ' ' or city_name_1 != '') and (city_name_2 != ' ' or city_name_2 != '') and request.split(' ')[3] != '':
                        get_distance(event.user_id, city_name_1, city_name_2)
                    else:
                        write_message(event.user_id, 'Вы ввели что-то не верно')
                    get_distance(event.user_id, city_name_1, city_name_2)
                elif request == 'как дела' or request == 'как дела?':
                    write_message(event.user_id, random.choice(pharse_howareyou))
                else:
                    write_message(event.user_id, random.choice(phrase_else))


main()