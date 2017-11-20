#import crypto
import base64
import json

# coding: utf-8
import sys, os, time, signal,thread
reload(sys)
sys.setdefaultencoding('utf-8')
import paho.mqtt.client as mqtt
client = None
mqtt_looping = False
TOPIC_ROOT = "lora/rxpk"
Key = '2b7e151628aed2a6abf7158809cf4f3c'

# redis
import redis_mq

#mongodb
from pymongo import MongoClient
import datetime

#Data cut
import data_cut


def mongo_insert(device,data):
    client = MongoClient('localhost', 27017)
    db = client['lora-server']
    data[0]["date"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "mongodb data ",type(data)
    db.sensor.insert_one({device:data}).inserted_id


def on_connect(mq, userdata, rc, _):
    # subscribe when connected.
    mq.subscribe(TOPIC_ROOT + '/#')

def on_message(mq, userdata, msg):
#    print "topic: %s" % msg.topic
#    print "payload: %s" % msg.payload
#    print "qos: %d" % msg.qos
    
    topic = msg.topic 
    code = ""
    sign = ""
#json decode to python is string
    data_de = json.loads(msg.payload)
    dd = data_de['data']
    rssi = data_de['rssi']
    lsnr = data_de['lsnr']
    freq = data_de['freq']
    
    for i in range(len(dd)):
        code = code+dd[i]
    print "Recieve data:",code
    
    sys.stdout.write("\033[0;32m")
    
#decode base64 in code
    decoded = base64.b64decode(code)
    print "Decode base64: ",decoded
    
    #cry=crypto.decodePHYpayload(decoded.encode("hex"),Key)
    
#convert ASCII code 
    decode = decoded.encode("hex")  
    print "Decode data : ",decode

#No ASCII code convert  
#    if len(decode) >= 128:
#if you want to demo (decode --> decoded and goto data_cut)
#        data = data_cut.yowa(decode,topic,rssi,lsnr,freq)
#        print "Yowa Data :",type(data)
#        print "Yowa Data : ",repr(data)
#        device='Yowa'
#        json_string=json.dumps(data)
#        red = redis_mq.pool(json_string)
#        red.push()    
    #elif len(decode) == 50 :
#if you want to demo (taifa1 --> taifa)
    data = data_cut.taifa1(code,topic,rssi,lsnr,freq)
    print "Taifa Data :",type(data)
    print "Taifa Data : ",repr(data)
    device="Taifa"
    json_string=json.dumps(data)
    red = redis_mq.pool(json_string)
    red.push()    
    #mongo_insert(device,data)
    

def mqtt_client_thread():
    global client, mqtt_looping
    client_id = "" # If broker asks client ID.
    client = mqtt.Client(client_id=client_id)

    # If broker asks user/password.
    user = ""
    password = ""
    client.username_pw_set(user, password)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        #client.connect("10.28.120.249",1883)
        client.connect("10.21.20.120",1883)
    except:
        print "MQTT Broker is not online. Connect later."

    mqtt_looping = True
    print "Looping..."

    #mqtt_loop.loop_forever()
    cnt = 0
    while mqtt_looping:
        client.loop()
        cnt += 1
        if cnt > 20:
            try:
                client.reconnect() # to avoid 'Broken pipe' error.
            except:
                time.sleep(1)
            cnt = 0

    print "quit mqtt thread"
    client.disconnect()

def stop_all(*args):
    global mqtt_looping
    mqtt_looping = False

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, stop_all)
    signal.signal(signal.SIGQUIT, stop_all)
    signal.signal(signal.SIGINT,  stop_all)  # Ctrl-C

    thread.start_new_thread(redis_mq.sub,())  # thread to publish Gateway
    
    mqtt_client_thread()

    print "exit program"
    sys.exit(0)

