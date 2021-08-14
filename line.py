import os

import requests

import credentials
from log import Log

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
LINE_NOTIFY_TOKEN = credentials.LINE_NOTIFY_TOKEN


class Notify:

    def __init__(self):
        self.send_cnt = 0
        self.logger = Log()

    def write_log_info(self, response):
        self.logger.log_info(msg=f'status code: {response.status_code}')
        self.logger.log_info(msg=f'response text: {response.text}')
        self.logger.log_info(msg=f'send count: {self.send_cnt}')

    def write_log_err(self, response):
        self.logger.log_error(msg=f'status code: {response.status_code}')
        self.logger.log_error(msg=f'response text: {response.text}')
        self.logger.log_error(msg=f'send count: {self.send_cnt}')

    def send_with_image(self, img, text):
        os.path.isfile(img)
        ret = requests.post(
            url=LINE_NOTIFY_URL,
            data={'message': text},
            headers={'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN},
            files={'imageFile': open(img, 'rb')}
        )
        if ret.status_code == 200:
            self.write_log_info(response=ret)
        else:
            self.write_log_err(response=ret)
        self.send_cnt += 1
        return ret

    def send_with_text(self, text):
        ret = requests.post(
            url=LINE_NOTIFY_URL,
            data={'message': text},
            headers={'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN},
        )
        if ret.status_code == 200:
            self.write_log_info(response=ret)
        else:
            self.write_log_err(response=ret)
        self.send_cnt += 1
        return ret


if __name__ == '__main__':
    notifier = Notify()
    notifier.send_with_image(img='tests/resources/1.png', text='test')
    notifier.send_with_text(text='test')
