from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
	return '疑問猫Botは正常です。この画面が表示されていない場合は製作者@kousakiraiにご連絡下さい'


def run():
	app.run(host="0.0.0.0", port=8080)


def keep_alive():
	server = Thread(target=run)
	server.start()
