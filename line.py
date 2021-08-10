import os
import datetime
import requests

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']


class Notify:

    def __init__(self):
        self.send_cnt = 0

    def _send(self, **kwargs):
        data = kwargs.get('data', None)
        file = kwargs.get('file', None)
        ret = requests.post(
            url=LINE_NOTIFY_URL,
            data=data,
            headers={'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN},
            files=file
        )
        self.send_cnt += 1
        return ret

    @staticmethod
    def _build_data(text):
        return {'message': text}

    @staticmethod
    def _build_file(img):
        os.path.isfile(img)
        return {'imageFile': open(img, 'rb')}

    def _record_response(self, text, res):
        send_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        f_name = f'log/log_{send_time}_{res.status_code}.txt'
        with open(f_name, 'a') as f:
            s = f"{send_time}({self.send_cnt}): {text} -> {res.status_code}, {res.text}\n"
            f.write(s)

    def send_with_image(self, img, text):
        data = self._build_data(text=text)
        file = self._build_file(img=img)
        res = self._send(data=data, file=file)
        self._record_response(text=text, res=res)

    def send_with_text(self, text):
        data = self._build_data(text=text)
        res = self._send(data=data)
        self._record_response(text=text, res=res)


if __name__ == '__main__':
    notifier = Notify()
    notifier.send_with_image(img='tests/resources/1.png', text='test')
    notifier.send_with_text(text='test')
