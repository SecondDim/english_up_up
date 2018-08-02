#! /usr/bin/python3

import os


class App:

    line_token = []

    def __init__(self):
        self.__set_token()
        """ TODO
            1. read
            2. choose
            3. check if have read.
            4. push notify
            5. write in data-log.json

            p.s. add welcome text in notify
        """

    def __set_token(self):
        with open('.env') as f:
            for e in f:
                self.line_token.append(e.strip())

    def had_read(self):
        pass

    def set_read(self):
        pass

    def get_list(self, folder='/'):
        pass

    def random_choose(self, number=1):
        pass

    def push_notify(self, wait=.5):
        pass

    def run(self):
        pass


if __name__ == '__main__':

    app = App()
    app.run()
