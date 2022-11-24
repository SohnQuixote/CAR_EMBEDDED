import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

load_dotenv()

firebase_key = os.environ.get('FIREBASE_KEY')
firebase_pw = os.environ.get('FIREBASE_PW')
firebase_url = os.environ.get('FIREBASE_URL')

cred = credentials.Certificate('firebase_key')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'firebase_url'
})

dir = db.reference()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))
    dir.update(mid)

def on_message(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))


# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
# on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# address : localhost, port: 1883 에 연결
client.connect("localhost", 1883)
# common topic 으로 메세지 발행
client.subscribe('common', 1)
client.loop_forever()
