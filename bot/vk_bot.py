from bot.settings import log
from bot.sql_control import add_user
from bot.words import msg_request, msg_response
from vk_api.longpoll import VkLongPoll, VkEventType
import bs4
import vk_api
import random
import requests


class VkBot:
    def __init__(self):
        self._user_id = None
        self._username = None
        self.vk = None

    @staticmethod
    def _get_user_name_from_vk_id(user_id):
        """ Парсит страницу пользователя с помощью BS4, получает имя и фамилию из title"""
        def _clean_all_tag_from_str(string_line):
            """ Очистка строки stringLine от тэгов и их содержимых
                Возвращает только строку с именеи и фамилией
            :param string_line: Очищаемая строка: <title>Имя Фамилия</title>
            :return: Очищенная строка: Имя фамилия
            """
            result = ""
            not_skip = True
            for elem in list(string_line):
                if not_skip:
                    if elem == "<":
                        not_skip = False
                    else:
                        result += elem
                else:
                    if elem == ">":
                        not_skip = True
            return result

        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = _clean_all_tag_from_str(bs.findAll("title")[0])
        return user_name.split()[0]

    def new_message(self, message):
        if message.lower() in msg_request['greeting']:
            return msg_response['greeting'].format(self._username)
        elif message.lower() in msg_request['main']:
            return msg_response['main']
        elif message.lower() in msg_request['get_money_list']:
            return msg_response['get_money_list']
        elif message.lower() in msg_request['how_to_get']:
            return msg_response['how_to_get']
        elif message.lower() in msg_request['questions']:
            return msg_response['questions']
        elif message.lower() in msg_request['not_approve']:
            return msg_response['not_approve']
        elif message.lower() in msg_request['thanks']:
            return msg_response['thanks']
        elif message.lower() in msg_request['bye']:
            return msg_response['bye']
        elif message.lower() in msg_request['not_necessary']:
            return msg_response['not_necessary'].format(self._username)
        elif message.lower() in msg_request['how_much_money']:
            return msg_response['how_much_money']
        else:
            return msg_response['default']

    def sender(self, event, message):
        if event.from_user:
            self.vk.messages.send(user_id=event.user_id, message=message, random_id=random.randint(100000, 999999))

    def connect(self):
        with open('bot/secret_keys.txt', mode='r') as file:
            token = file.readline()[:-1]
            group_id = int(file.readline())
        try:
            vk_session = vk_api.VkApi(token=token)
            long_poll = VkLongPoll(vk_session, group_id)
            self.vk = vk_session.get_api()
            return long_poll
        except ConnectionError:
            log.error('Connection Error')
            return

    def run(self):
        long_poll = self.connect()
        if not long_poll:
            return 0
        for event in long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self._user_id = event.user_id
                add_user(self._user_id)
                self._username = self._get_user_name_from_vk_id(event.user_id)
                msg = self.new_message(event.text)
                print(event.user_id, event.text)
                self.sender(event, msg)
