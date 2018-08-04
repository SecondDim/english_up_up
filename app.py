#! /usr/bin/python3

import os
import sys
import json
import time
import random
import requests


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class App:

    line_token = []
    vocabulary_list = []
    request_headers = {}

    folder = ''
    date_file = ''

    had_read_num = 0
    token_index = 0
    history_file_path = sys.path[0] + '/history.json'
    line_notify_url = 'https://notify-api.line.me/api/notify'

    def __init__(self, date_file, folder):
        self.token_index = random.randint(0, 10)

        self.__set_token()
        self.set_header()

        self.folder = folder
        self.date_file = date_file

        if not os.path.exists(self.history_file_path):
            with open(self.history_file_path, 'w') as f:
                json.dump([], f)

        """ TODO
            4. push notify
            p.s. add welcome text in notify
        """

    def __set_token(self):
        with open(sys.path[0] + '/.env') as f:
            for e in f:
                self.line_token.append(e.strip())

    def set_header(self):
        self.token_index = (self.token_index + 1) % len(self.line_token)
        self.request_headers = {
            'Authorization': 'Bearer ' + self.line_token[self.token_index],
        }

    def get_list(self):
        try:
            with open(sys.path[0] + '/data/' + self.folder + self.date_file) as f:
                for w in f:
                    self.vocabulary_list.append(w.strip())
        except Exception as e:
            print(bcolors.FAIL +
                  "[Error] Get vocabulary file not exist or read error. Msg:"
                  + str(e)
                  + bcolors.ENDC)
            sys.exit(0)

    def had_read(self):
        try:
            with open(self.history_file_path) as f:
                old_read = json.load(f)
                self.had_read_num = len(old_read)
                for o in old_read:
                    if o in self.vocabulary_list:
                        self.vocabulary_list.remove(o)
        except Exception as e:
            print(bcolors.FAIL +
                  "[Error] Read history file process error. Msg:"
                  + str(e)
                  + bcolors.ENDC)
            sys.exit(0)

    def set_read(self, voc):
        try:
            with open(self.history_file_path, 'r') as f:
                old_read = json.load(f)

            [old_read.append(x) for x in voc]

            with open(self.history_file_path, 'w') as f:
                json.dump(old_read, f)

        except Exception as e:
            print(bcolors.FAIL +
                  "[Error] Set history file process error. Msg:"
                  + str(e)
                  + bcolors.ENDC)
            sys.exit(0)

    def random_choose(self, number=1):
        return random.choices(self.vocabulary_list, k=number)

    def welcome(self):
        content = ("背單字囉~成功是持續的成果！\n來源字典：%s\n已背單字：%s" %
                   (
                       str(self.folder + self.date_file),
                       str(self.had_read_num))
                   )

        self.push_notify(content)

    def vocabulary_message(self, voc):
        self.welcome()
        for v in voc:
            self.push_notify(v)

    def push_notify(self, content):
        # print(content)
        # return True
        r = requests.post(self.line_notify_url,
                          headers=self.request_headers,
                          params={'message': content})

        return r

    def run(self):
        self.get_list()
        self.had_read()

        voc = self.random_choose(number=3)
        self.vocabulary_message(voc)

        self.set_read(voc)


if __name__ == '__main__':
    folder = 'TOEIC/'
    date_file = "basic1000.txt"

    if len(sys.argv) > 2 and sys.argv[1]:
        folder = sys.argv[1] + '/'
        if len(sys.argv) > 3 and sys.argv[2]:
            date_file = sys.argv[2]

    try:
        if not os.path.isfile(sys.path[0] + '/data/' + folder + date_file):
            raise IOError

        app = App(folder=folder, date_file=date_file)
        app.run()
    except Exception as e:
        print(bcolors.FAIL +
              "[Error] Init error."
              + str(e)
              + bcolors.ENDC)
