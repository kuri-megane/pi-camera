import datetime
import os
import time

from camera import Camera
from image_diff import ImageDiff
from log import Log
from slack import Notify

# 現在の設定では1実行60分，約15秒周期で監視
INTERVAL = 60 * 4
DIFF_SEC = 14


def main():
    logger = Log()
    camera = Camera(logger=logger)
    differ = ImageDiff(logger=logger)
    notifier = Notify(logger=logger)

    notifier.send_with_text(text='監視カメラが作動し始めました')
    logger.log_info(msg='監視カメラ スタート')

    # 保存先の作成
    today = datetime.datetime.today().strftime('%Y%m%d')
    os.makedirs(name=f'./data/{today}', exist_ok=True)

    c = 0
    while c < INTERVAL:

        now = datetime.datetime.now().strftime('%H%M%S')

        # 1枚目の取得
        before_file = f'./data/{today}/{now}_0.png'
        camera.capture(save_path=before_file)

        # 待機
        time.sleep(DIFF_SEC)

        # 2枚目の取得
        after_file = f'./data/{today}/{now}_1.png'
        camera.capture(save_path=after_file)

        # 差分確認
        is_diff = differ.check(before_img=before_file, after_img=after_file)

        # 通知
        if is_diff:
            logger.log_info(msg='差分あり')
            notifier.send_with_image(text=now, img=after_file)
        else:
            logger.log_info(msg='差分なし')

        c += 1

    notifier.send_with_text(text='監視カメラが終了しました')
    logger.log_info(msg='監視カメラ 終了')


if __name__ == '__main__':
    main()
