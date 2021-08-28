import cv2

from log import Log

# 使用するカメラを指定 0が内蔵
DEVICE_ID = 0


class Camera:

    def __init__(self, **kwargs):
        self.camera = None
        self.frame = None

        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = Log()

    def _open(self):
        self.camera = cv2.VideoCapture(DEVICE_ID)

    def _get(self):
        # カメラの準備ができているか
        if not self.camera.isOpened():
            self.logger.log_error('カメラオープンエラー')
            return

        # 読み込み
        ret, self.frame = self.camera.read()

        # 撮影失敗時
        if not ret:
            self.frame = None
            self.logger.log_error('撮影失敗 ret false')
            return
        if self.frame is None:
            self.logger.log_error('撮影失敗 frame 空')
            return

    def _save(self, save_path):
        if self.frame is None:
            self.logger.log_error('画像保存失敗')
            return
        cv2.imwrite(filename=save_path, img=self.frame)

    def _close(self):
        self.camera = None

    def capture(self, save_path):
        self._open()
        self._get()
        self._save(save_path)
        self._close()


if __name__ == '__main__':
    camera = Camera()
    camera.capture(save_path='tests/data/hoge.png')
