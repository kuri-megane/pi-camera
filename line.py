import os
import requests

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']


class Notify:

    def __init__(self):
        self.send_img = None
        self.send_txt = {'message': 'err'}

    def _send(self):
        ret = requests.post(
            url=LINE_NOTIFY_URL,
            data=self.send_txt,
            headers={'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN},
            files=self.send_img
        )
        return ret

    def _text(self, text):
        self.send_txt = {'message': text}

    def _img(self, img):
        os.path.isfile(img)
        self.send_img = {'imageFile': open(img, 'rb')}

    def _record_response(self, text, res):
        f_name = f'log/log_{text}_{res.status_code}.txt'
        with open(f_name, 'w') as f:
            s = f"{self.send_txt} :-> {res.status_code}, {res.text}"
            f.write(s)

    def send_with_image(self, img, text):
        self._text(text=text)
        self._img(img=img)
        res = self._send()
        self._record_response(text=text, res=res)

    def send_with_text(self, text):
        self._text(text=text)
        res = self._send()
        self._record_response(text=text, res=res)


if __name__ == '__main__':
    notifier = Notify()
    notifier.send_with_image(img='tests/resources/1.png', text='test')
