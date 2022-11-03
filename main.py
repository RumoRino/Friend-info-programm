import csv
import pprint
import requests

token = input("Введите авторизационный токен: ")
user_id = input("Введите ID пользователя: ")

def friends(token, user_id):
    token = token
    version = 5.131
    user_id = user_id

    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'user_id': user_id,
                                'order': 'name',
                                'fields': 'country, city, bdate, sex'

                            }
                            )
    friends = response.json()['response']['items']
    return friends

def file_writer(friends):
    with open('report.csv', 'w') as file:
        data = csv.writer(file)
        data.writerow((
            'first_name',
            'last_name',
            'country',
            'city',
            'bdate',
            'sex'
        ))

        for friend in friends:
            try:
                if friend['country']['title']:
                    country = friend['country']['title']
                else:
                    country = 'Страна не указана'
            except:
                country = '<Страна не указана>'

            try:
                if friend['city']['title']:
                    city = friend['city']['title']
                else:
                    city = 'Город не указан'
            except:
                city = '<Город не указан>'

            try:
                if friend['sex'] == 1:
                    sex = 'Жен.'
                elif friend['sex'] == 2:
                    sex = 'Муж.'
                else:
                    sex = 'Пол не указан'
            except:
                sex = '<Пол не указан>'

            try:
                if friend['bdate']:
                    bdate = friend['bdate']

                else:
                    bdate = 'Дата не указана'
            except:
                bdate = '<Дата не указана>'

            data.writerow((
                friend['first_name'],
                friend['last_name'],
                country,
                city,
                bdate,
                sex))

friend_list = friends(token, user_id)
file_writer(friend_list)

print('Отчёт сформирован')