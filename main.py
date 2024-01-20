from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
from sensor import Root
from bot import send
# import requests
from flask_cors import CORS
import json
from cryptography.fernet import Fernet
from flask_apscheduler import APScheduler
import redis
import asyncio

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())
db = redis.Redis(username='default', password='redispw', port=32768) #connect to server
scheduler = APScheduler()
CORS(app)
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = '/eic/insania'
alert_emoji = u"\U0001F6A8"
mqtt_client = Mqtt(app)

# cipher_key = Fernet.generate_key()
cipher_key = b'1QSK0jIO81QMhmncWvFFjDl56Egct0n7KqmF2fzsEIk='
my_token = '5838292226:AAHSlJxlz0Aw5DNSPerP0R9yxFLNv1xePS4'
print(cipher_key)
cipher = Fernet(cipher_key)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   decrypted_message = cipher.decrypt(message.payload) 
   data = dict(
       topic=message.topic,
       payload=str(decrypted_message.decode("utf-8"))
  )
#    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
   jsonstring = json.loads(str(decrypted_message.decode("utf-8")))
   root = Root.from_dict(jsonstring)
   
   tele_message = '\U0001F6A8 \U0001F6A8 \U0001F6A8 ALERT \U0001F6A8 \U0001F6A8 \U0001F6A8 \n Network status is DOWN!!! \n\n'
   cnt = 1
   for sensor in root.sensors:
     if db.exists(sensor.device) and (sensor.sensor.lower() not in "ping"):
        continue
     tele_message += '{cnt}. {sensor.device} \n'.format(cnt=cnt, sensor=sensor)
     cnt+=1
     db.setex(name=sensor.device, time=60, value=sensor.device)
    #  asyncio.run(send("Integrated Smart Network Issue Alarm (InSaNIA), an early detection system that help us to monitor and report any emergency network issues in PTKP real-time, and available 24/7. This message is automated", -1001903139828, my_token))
   tele_message += '\n PLEASE CHECK'
   cnt = 0
   print(tele_message)
   asyncio.run(send(tele_message, -1001903139828, my_token))


# @app.route('/sensors', methods=['GET'])
# def publish_message():
#    res = requests.get("https://172.21.73.119/api/table.json?content=sensors&output=json&columns=objid,device,sensor,status&username=pcnetwork&password=P@ssw0rd&filter_status=5", verify=False)
#    encrypted_message = cipher.encrypt(bytes(res.text, 'utf-8'))
#    out_message = encrypted_message.decode()# turn it into a string to send
#    publish_result = mqtt_client.publish(topic, out_message)
#    return jsonify({'code': publish_result[0], 'message': out_message})

# @scheduler.task('interval', id='publish_message_down sensor', seconds=60, misfire_grace_time=900)
# def publish_message_schedule():
#    res = requests.get("https://172.21.73.119/api/table.json?content=sensors&output=json&columns=objid,device,sensor,status&username=pcnetwork&password=P@ssw0rd&filter_status=5", verify=False)
#    encrypted_message = cipher.encrypt(bytes(res.text, 'utf-8'))
#    out_message = encrypted_message.decode()# turn it into a string to send
#    publish_result = mqtt_client.publish(topic, out_message)
#    print("Published")
#    return jsonify({'code': publish_result[0], 'message': out_message})

# scheduler.init_app(app)
# scheduler.start()

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
