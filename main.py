import csv
import json
import requests
import argparse

parser = argparse.ArgumentParser(
    prog='Find the friends',

    description='Для того, чтобы сформировать отчёт нужно использовать access token и ID пользователя,'
                ' у которого будем брать список друзей. Access token можно получить создав приложение в вк или'
                'перейдя по ссылке https://vkhost.github.io, и выбрав приложение vk.com. Id пользователя '
                'можно взять с личного профиля вконтакте или же найти в настройках профиля. '
                'Следующим аргументом должно идти название файла. Последним аргументом указывается формат отчёта. '
                'Доступны 3 формата: csv (задан по умолчанию), json и tsv. Если не указывать формат, то отчёт будет '
                'сформирован в формате csv. Пример: python main.py -t <token> -uid <user id> -fn <file name> -form json',

    epilog='Enjoy using it')

token = parser.add_argument("-t", "--token",
                            action='store',
                            help='1. Токен, обязательный')

user_id = parser.add_argument("-uid", "--user-id",
                              action='store',
                              help='2. Id пользователя, обязательный')

file_name = parser.add_argument("-fn", "--file-name",
                                action='store',
                                help='3. Имя файла, обязательный',
                                type=str)

form = parser.add_argument("-form", "--file-format",
                           help='4. Формат отчёта, необязательный. Допустимые форматы: csv, tsv, json.'
                                ' Стандартный формат - csv.',
                           default = "csv")

args = parser.parse_args()


def friends(token, user_id):

    version = 5.131

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

def file_writer_json(friends, file_name, format):
    jsonFriends = json.dumps(friends, ensure_ascii = False).encode('utf8')
    jsonFriends = json.loads(str(jsonFriends.decode()))
    with open(f"{file_name}.{format}", 'w', encoding = 'utf-8') as file:
        json.dump(jsonFriends, file, indent = 4, ensure_ascii = False)

def file_writer_csv(friends, file_name, format):
    with open(f"{file_name}.{format}", 'w') as file:
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


try:
    friend_list = friends(args.token, args.user_id)

    if args.file_format == "tsv":

        print('Данный формат фала пока не поддерживается.')
        # file_writer(friend_list, args.file_name, "tsv")
        # print('Отчёт сформирован')

    elif args.file_format == "json":

        file_writer_json(friend_list, args.file_name, "json")
        print('Отчёт сформирован')

    elif args.file_format == "csv":

        file_writer_csv(friend_list, args.file_name, "csv")
        print('Отчёт сформирован')

    else:

        print('Неверный формат файла. Отчёт будет сформирован в стандартном формате.')
        file_writer_csv(friend_list, args.file_name, "csv")

except:

    print('Неверно указаны аргументы. Используйте "-h" или "--help"')
