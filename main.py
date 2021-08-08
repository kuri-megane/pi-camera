from camera import Camera
from image_diff import ImageDiff
from line import Notify

import time
import datetime


def main():

    camera = Camera()
    differ = ImageDiff()
    notifier = Notify()

    while True:
        # 1枚目の取得
        before_time = datetime.datetime.now().strftime('%H:%M:%S')
        before_file = f'data/{before_time}.png'
        camera.capture(save_path=before_file)

        # 待機
        time.sleep(10)

        # 2枚目の取得
        after_time = datetime.datetime.now().strftime('%H:%M:%S')
        after_file = f'data/{after_time}.png'
        camera.capture(save_path=after_file)

        # 差分確認
        is_diff = differ.check(before_img=before_file, after_img=after_file)

        # 通知
        if is_diff:
            notifier.send_with_image(text=after_time, img=after_file)


if __name__ == '__main__':
    main()
