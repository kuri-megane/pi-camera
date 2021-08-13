import datetime
import os

import requests

SLACk_URL = 'https://slack.com/api/'
SLACK_MESSAGE_ENDPOINT = 'chat.postMessage'
SLACK_FILE_ENDPOINT = 'files.upload'
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_TOKEN = os.environ['SLACK_TOKEN']


class Notify:

    def __init__(self):
        self.send_cnt = 0

    def _record_response(self, text, res):
        send_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        f_name = f'log/log_{send_time}_{res.status_code}.txt'
        with open(f_name, 'a') as f:
            s = f"{send_time}({self.send_cnt}): {text} -> {res.status_code}, {res.text}\n"
            f.write(s)

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
        self.send_cnt += 1
        return ret


if __name__ == '__main__':
    notifier = Notify()
    r = notifier.send_with_image(img='tests/resources/1.png', text='test')
    print(r.status_code)
    print(r.headers)
    print(r.content)
    notifier._record_response(text='test', res=r)
    notifier.send_with_text(text='test')
