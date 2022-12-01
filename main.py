import configparser

from telethon.sync import TelegramClient
import sqlite3

import time

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest



URL = [] #ссылки на чаты
WORDS = ['Работ', 'робот', 'вакан','Обязанности','требуется','Склад','набор','Набираем'] #Ключевые слова

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']



with TelegramClient('egoisteq',api_id, api_hash) as client:
    client.session.save()

client.start()







async def dump_all_messages(channel, url):
    user_list = []
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 100   # максимальное число записей, передаваемых за один раз
    total_count_limit = 5000  # поменяйте это значение, если вам нужны не все сообщения
    
    
    while True:
        try:
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                return user_list
            messages = history.messages
            for message in messages:       
                msg_text = message.to_dict()
                try:
                    user = await client.get_entity(msg_text["from_id"]["user_id"])
                    user = user.to_dict()
                    username = user['username']

                    if username and user['bot'] == False:
                        username = f'@{username}\n'
                        user_list.append(str(username))

                except Exception as _ex:
                    pass

            offset_msg = messages[len(messages) - 1].id
            if len(user_list) >= total_count_limit:
                return user_list

        except Exception as _ex:
            print(_ex)
            



async def main():
    res_list = []
    for url in URL:
        channel = await client.get_entity(url)
        user_list = await dump_all_messages(channel, url)
        for a in user_list:
            res_list.append(a)

        
        


    with open("invajt_done.txt ", "r") as file: #проверка на прошлый парсинг
        list1 = file.readlines()
    lst = res_list
    res_list = []
    for user in lst:
        if user not in list1:
            res_list.append(user)

    res_list_sort = []
    for user in res_list:
        if user not in res_list_sort:
            res_list_sort.append(user)
    
    res_list.sort()
    res_list_sort.sort()


    connection = sqlite3.connect("Userss_message1.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Userss_message1 (username TEXT , numbers INTEGER)")

    n = 0
    while True:
        try:
            if res_list_sort[0] == res_list[0]:
                del res_list[0]
                n += 1
            else:
                cursor.execute(f"INSERT INTO Userss_message1 VALUES ('{res_list_sort[0]}', '{n}')")
                n = 0
                del res_list_sort[0]
        except Exception as _ex:
            print(_ex)
            break

    connection.commit()
    connection.close()





with client:
    client.loop.run_until_complete(main())


