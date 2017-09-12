import crypto
import base64
import json
# coding: utf-8
import sys, os, time, signal
reload(sys)
sys.setdefaultencoding('utf-8')
import paho.mqtt.client as mqtt
client = None
mqtt_looping = False
TOPIC_ROOT = "lora/rxpk"
Key = '2b7e151628aed2a6abf7158809cf4f3c'
# redis
import redis_push

#mongodb
from pymongo import MongoClient
import datetime

def mongo_insert(data):
    client = MongoClient('localhost', 27017)
    db = client['lora-server']
    data[0]["date"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print type(data)
    db.sensor.insert_one({"taifa_device":data}).inserted_id

def on_connect(mq, userdata, rc, _):
    # subscribe when connected.
    mq.subscribe(TOPIC_ROOT + '/#')

def on_message(mq, userdata, msg):
#    print "topic: %s" % msg.topic
#    print "payload: %s" % msg.payload
#    print "qos: %d" % msg.qos
    code = ""
    sign = ""
    rssi = data_de['rssi']
    lsnr = data_de['lsnr']
    freq = data_de['freq']
    #json decode to python is string
    data_de = json.loads(msg.payload)
    dd = data_de['data']
    for i in range(len(dd)):
        code = code+dd[i]
    print code
    
#decode base64 in code
    decoded = base64.b64decode(code)
    cry=crypto.decodePHYpayload(decoded.encode("hex"),Key)
    decode = cry.getdata()
    print decode
    decode =decode.split(',')
    if len(he(int(decode[1]))):
        idd = "0"+he(int(decode[1]))
    else:
        idd = he(int(decode[1]))
    typ = decode[0]
    battery = he(int(decode[7]))
    longitude = decode[8]
    latitude = decode[12]
    x = decode[16]
    y = decode[18]
    z = decode[20]
    Sos = decode[22]
    status = he(int(decode[23]))
    check = he(int(decode[24]))
    for i in xrange(1,6):
        idd = idd +":"+ he(int(decode[i+1]))
    for i in xrange(1,4):
        longitude = longitude + decode[i+8]
        latitude = latitude + decode[i+12] 
    print longitude
    print latitude
    if decode[16] == "0":
        sign = "+"
        x = sign +","+ str(float(decode[17])/100)
    else:
        sign = "-"
        x = sign +","+ str(float(decode[17])/100)
    if decode[18] == "0":
        sign = "+"
        y = sign +","+ str(float(decode[19])/100)
    else:
        sign = "-"
        y = sign +","+ str(float(decode[19])/100)
    if decode[20] == "0":
        sign = "+"
        z = sign +","+ str(float(decode[21])/100)
    else:
        sign = "-"
        z = sign +","+ str(float(decode[21])/100)
    lng = float(longitude)/100000.0        
    lat = float(latitude)/100000.0
    
    if decode[11] == "0":
        lng = "+"+str(lng)
    else:
        lng = "-"+str(lng)
    if decode[15] == "0":
        lat = "+"+str(lat)
    else:
       lat = "-"+str(lat)
    
    data =[{ " node_id " : idd ,
            " battery " : battery ,
            " lng " : lng ,
            " lat " : lat ,
            " 3-axis " : { 
                            " X " : x ,
                            " Y " : y ,
                            " Z " : z ,
                          }, 
            " SoS " : Sos ,
            " status " : status ,
            " check_sum " : check ,
            " source " : msg.topic ,
            " type " : " 0x02 " ,
            " gateway_id " : " d8:b9:0e:00:12:21 " ,
            "rssi": rssi,
            "lsnr": lsnr,
            "freq": freq
            }]
    
    print "Data: ",repr(data)

    #json_string=json.dumps(data)
    #print json_string 
    #red = redis_push.pool(transdata)#json_string)
    #red.push()    
    
    mongo_insert(data)

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
        client.connect("10.28.120.249",1883)
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

    mqtt_client_thread()

    print "exit program"
    sys.exit(0)

