# pi-camera

RaspberryPiを監視カメラにするスクリプト

## Requirements
- python3 >= 3.7

## Install

### ubuntu

```shell
sudo apt install python3-pip
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Raspberry Pi

opencvのバージョンが異なるため，別途別バージョンを入れます．

cf. 1. [RaspberryPiへのOpenCVインストール手順](https://qiita.com/wk_/items/8db529a6b24a955888db)

opencvのインポートに失敗するときはこちらを参考にしました．

cf. 2. [【Raspberry Pi】Raspberry Pi Zero WにOpenCVの環境を構築する](https://rikoubou.hatenablog.com/entry/2019/05/21/151337)


下記には，OS直の環境にpython実行環境を用意する例を残します．

```shell
sudo apt install python3-pip
pip3 install -r requirements.txt
# 不足する依存物 (1つ目のサイトに記載)
sudo apt install libavutil56 libcairo-gobject2 libgtk-3-0 libqtgui4 libpango-1.0-0 libqtcore4 libavcodec58 libcairo2 libswscale5 libtiff5 libqt4-test libatk1.0-0 libavformat58 libgdk-pixbuf2.0-0 libilmbase23 libjasper1 libopenexr23 libpangocairo-1.0-0 libwebp6
# 不足する依存物 (2つ目のサイトに記載)
sudo apt install libatlas-base-dev
# opencv再インストール
pip3 install opencv-python==4.1.0.25
```
