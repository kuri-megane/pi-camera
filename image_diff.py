import os.path

import cv2
import numpy as np

from log import Log

# 二値化のしきい値 夕焼けなどの影響を防ぎたい
BINARY_THRESHOLD = 60
# 膨張収縮の近傍画素指定 2:4近傍, 3:8近傍
MASK_SIZE = 4
# 差分があったと判定する画素数の割合
COUNT_THRESHOLD = 0.1


class ImageDiff:

    def __init__(self, **kwargs):
        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = Log()

    @staticmethod
    def _read(img_path):
        os.path.isfile(img_path)
        c_img = cv2.imread(filename=img_path)
        g_img = cv2.cvtColor(src=c_img, code=cv2.COLOR_BGR2GRAY)
        return g_img

    @staticmethod
    def _convert_diff_img(before_img, after_img):
        # 差分抽出
        diff = cv2.absdiff(before_img, after_img)
        # 二値化処理
        _, binary = cv2.threshold(src=diff, thresh=BINARY_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY, dst=None)
        # 膨張収縮処理
        operator = np.ones((MASK_SIZE, MASK_SIZE), np.uint8)
        erode = cv2.erode(binary, operator, iterations=4)
        dilate = cv2.dilate(erode, operator, iterations=4)
        return dilate

    def _is_diff(self, binary_img):
        # 差分画素のカウント
        count = np.sum(binary_img) / 255
        self.logger.log_info(msg=f'差分カウント: {count}')
        # 割合算出
        percentage = count / np.size(binary_img)
        self.logger.log_info(msg=f'差分割合: {percentage}')
        # 判定
        if percentage > COUNT_THRESHOLD:
            return True
        return False

    def check(self, before_img, after_img):
        before_img = self._read(img_path=before_img)
        after_img = self._read(img_path=after_img)
        binary_img = self._convert_diff_img(before_img=before_img, after_img=after_img)
        return self._is_diff(binary_img=binary_img)


if __name__ == '__main__':
    differ = ImageDiff()
    b_img = differ._read(img_path='tests/resources/1.png')
    a_img = differ._read(img_path='tests/resources/2.png')
    d_img = differ._convert_diff_img(before_img=b_img, after_img=a_img)
    ret = differ._is_diff(binary_img=d_img)
    print(ret)
    cv2.imshow('before_img', b_img)
    cv2.imshow('after_img', a_img)
    cv2.imshow('dilate_img', d_img)
    cv2.waitKey(0)
