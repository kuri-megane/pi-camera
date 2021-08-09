from camera import Camera
from image_diff import ImageDiff
from line import Notify

import time
import datetime

# 現在の設定では1実行30分，15秒周期で監視
INTERVAL = 30 * 2
DIFF_SEC = 29


def main():

    camera = Camera()
    differ = ImageDiff()
    notifier = Notify()

    notifier.send_with_text(text='監視カメラが作動し始めました')
    print('監視カメラ スタート')

    c = 0
    while c < INTERVAL:
        # 1枚目の取得
        before_time = datetime.datetime.now().strftime('%H:%M:%S')
        before_file = f'data/{before_time}.png'
        camera.capture(save_path=before_file)

        # 待機
        time.sleep(DIFF_SEC)

        # 2枚目の取得
        after_time = datetime.datetime.now().strftime('%H:%M:%S')
        after_file = f'data/{after_time}.png'
        camera.capture(save_path=after_file)

        # 差分確認
        is_diff = differ.check(before_img=before_file, after_img=after_file)

        # 通知
        if is_diff:
            print('差分あり')
            print(after_time)
            notifier.send_with_image(text=after_time, img=after_file)

        c += 1

    notifier.send_with_text(text='監視カメラが終了しました')
    print('監視カメラ スタート')


if __name__ == '__main__':
    main()
