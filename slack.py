import requests

import credentials
from log import Log

SLACk_URL = 'https://slack.com/api/'
SLACK_MESSAGE_ENDPOINT = 'chat.postMessage'
SLACK_FILE_ENDPOINT = 'files.upload'
SLACK_CHANNEL = credentials.SLACK_CHANNEL
SLACK_TOKEN = credentials.SLACK_TOKEN


class Notify:

    def __init__(self, **kwargs):
        self.send_cnt = 0

        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = Log()

    def send_with_image(self, img, text):
        ret = requests.post(
            url=SLACk_URL + SLACK_FILE_ENDPOINT,
            data={
                'channels': SLACK_CHANNEL,
                'filename': f'{text}.png',
                'initial_comment': text,
            },
            headers={'Authorization': 'Bearer ' + SLACK_TOKEN},
            files={
                'file': open(img, 'rb'),
            }
        )
        self.logger.log_info(msg=f'status code: {ret.status_code}')
        self.logger.log_info(msg=f'response text: {ret.text}')
        self.logger.log_info(msg=f'send count: {self.send_cnt}')
        self.send_cnt += 1
        return ret

    def send_with_text(self, text):
        ret = requests.post(
            url=SLACk_URL + SLACK_MESSAGE_ENDPOINT,
            data={
                'channel': SLACK_CHANNEL,
                'text': text
            },
            headers={'Authorization': 'Bearer ' + SLACK_TOKEN},
        )
        self.logger.log_info(msg=f'status code: {ret.status_code}')
        self.logger.log_info(msg=f'response text: {ret.text}')
        self.logger.log_info(msg=f'send count: {self.send_cnt}')
        self.send_cnt += 1
        return ret


if __name__ == '__main__':
    notifier = Notify()
    r = notifier.send_with_image(img='tests/resources/1.png', text='test')
    print(r.status_code)
    print(r.headers)
    print(r.content)
    notifier.send_with_text(text='test')
