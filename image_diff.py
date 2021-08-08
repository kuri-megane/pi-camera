import os.path
import cv2
import numpy as np

# 二値化のしきい値 夕焼けなどの影響を防ぎたい
BINARY_THRESHOLD = 10
# 膨張収縮の近傍画素指定 2:4近傍, 3:8近傍
MASK_SIZE = 3
# 差分があったと判定する画素数の割合
COUNT_THRESHOLD = 0.1


class ImageDiff:

    def __init__(self):
        self.before_img = None
        self.after_img = None
        self.result_img = None

    def _read(self, before_img, after_img):
        os.path.isfile(before_img)
        os.path.isfile(after_img)
        self.before_img = cv2.imread(filename=before_img)
        self.after_img = cv2.imread(filename=after_img)

    def _convert_diff_img(self):
        # グレースケール変換
        self.before_img = cv2.cvtColor(src=self.before_img, code=cv2.COLOR_BGR2GRAY)
        self.after_img = cv2.cvtColor(src=self.after_img, code=cv2.COLOR_BGR2GRAY)

        # 差分抽出
        diff = cv2.absdiff(self.before_img, self.after_img)
        # 二値化処理
        _, binary = cv2.threshold(src=diff, thresh=BINARY_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY, dst=None)
        # 膨張処理・収縮処理
        operator = np.ones((MASK_SIZE, MASK_SIZE), np.uint8)
        erode = cv2.erode(binary, operator, iterations=4)
        self.result_img = cv2.dilate(erode, operator, iterations=4)

    def _count(self):
        # 差分画素のカウント
        count = np.sum(self.result_img) / 255
        # 割合算出
        percentage = count / np.size(self.result_img)
        # 判定
        if percentage > COUNT_THRESHOLD:
            return True
        return False

    def check(self, before_img, after_img):
        self._read(before_img=before_img, after_img=after_img)
        self._convert_diff_img()
        return self._count()


if __name__ == '__main__':
    differ = ImageDiff()
    _ = differ.check(before_img='tests/resources/1.png', after_img='tests/resources/2.png')
    cv2.imshow('check debug', differ.result_img)
    cv2.waitKey(0)

