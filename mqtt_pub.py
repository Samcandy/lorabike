# coding: utf-8
import sys, os, time
reload(sys)
sys.setdefaultencoding('utf-8')

import paho.mqtt.client as mqtt

import base64
import json
import datetime
import random
# If broker asks client ID.
client_id = ""

client = mqtt.Client(client_id=client_id)

# If broker asks user/password.
user = ""
password = ""
client.username_pw_set(user, password)

#client.connect("10.28.120.249",1883)
client.connect("10.21.20.120")
count = 0

def taifa_v(count):
    typ = "01"
    mac="20160003"
    i,j,start1,start2=0,0,0.149787,0.683765
    sos="0000"
    status="0000"
    check_sum="0021"
    x=str(format(int("3d",16)+random.randint(-5,15),'04X'))
    y=str(format(int("56",16)+random.randint(-15,30),'04X'))
    z=str(format(int("4c",16)+random.randint(-10,10),'04X'))
    
    
    #lng="00000000"
    #lat="00000000"
    if count >=0 and count<11:
        start1=0.149787
        start2=0.683765     
        i = (0.150302-0.149787)/10
        j = (0.684008-0.683765)/10
    elif count < 26 and count >10:
        i=(0.150520-0.150302)/15
        j=(0.683475-0.684008)/15
        start1=0.150302
        start2=0.684008
        count -=10
    elif count <36 and count>25:
        i=(0.149987-0.150520)/10
        j=(0.683217-0.683475)/10
        start1=0.150570
        start2=0.683367
        count -=25
    elif count <51 and count>35:
        i=(0.149810-0.150017)/15
        j=(0.683705-0.683163)/15
        start1=0.150017
        start2=0.683163
        count -=35
    else :
        i=0
        j=0
        sos="0001"
        x="0040"
        y="013c"
        z="001d"
    lat=(start1+i*count)*1000000
    lng=(start2+j*count)*1000000


    battery= str(int(99-count/30))


    data=typ+mac+battery+str(24)+str(int(lat))+str(78)+str(int(lng))+x+y+z+sos+status+check_sum
    #data=typ+mac+battery+lng+lat+x+y+z+sos+status+check_sum
    print data
    data_b64 = base64.b64encode(data)

    print data_b64

    return data_b64

def yowa_v(count):
    typ = "01"
    mac="070707080808"
    i,j,start1,start2=0,0,0.149865,0.684069
    sos="0000"
    status="0000"
    check_sum="0000"
    x=format(int("2a",16)+random.randint(-5,15),'02X')
    y=format(int("c1",16)+random.randint(-15,30),'02X')
    z=format(int("30",16)+random.randint(-10,10),'02X')
    
    
    x="2b"+str(x)
    y="2b"+str(y)
    z="2b"+str(z)

    #lng="00000000"
    #lat="00000000"
    if count >=0 and count<11:
        start1=0.149865
        start2=0.684069     
        i = (0.149531-0.149865)/10
        j = (0.685121-0.684069)/10
    elif count < 26 and count >10:
        i=(0.150498-0.149531)/15
        j=(0.685495-0.685121)/15
        start1=0.149531
        start2=0.685121
        count -=10
    elif count <36 and count>25:
        i=(0.150720-0.150498)/10
        j=(0.684448-0.685495)/10
        start1=0.150498
        start2=0.685495
        count -=25
    elif count <46 and count>35:
        i=(0.149865-0.150720)/10
        j=(0.684069-0.684448)/10
        start1=0.150720
        start2=0.684448
        count -=35
    else :
        i=0
        j=0
        sos="0001"
        x="2b40"
        y="2d3c"
        z="2b1d"
    lat=(start1+i*count)*1000000
    lng=(start2+j*count)*1000000


    battery= format(int(89-count/30),'02X')
    

    data="50494E47"+typ+mac+str(battery)+str(24)+str(int(lat))+str(78)+str(int(lng))+x+y+z+sos+status+check_sum+"202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F"
    #data=typ+mac+battery+lng+lat+x+y+z+sos+status+check_sum
    print data
    print len(data)
    data_b64 = base64.b64encode(data)

    print data_b64

    return data_b64

while 1:
    ta_payload = {
        "tmst":1084377236,
        "time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chan":3,
        "rfch":0,
        "freq":923.600000,
        "stat":1,
        "modu":"LORA",
        "datr":"SF10BW125",
        "codr":"4/5",
        "lsnr":format(random.uniform(1,10),'.1f'),
        "rssi":random.randint(-86,-68),
        "size":24,
        "data":taifa_v(count)} 
    
    yo_payload = {
        "tmst":1084377222,
        "time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chan":3,
        "rfch":0,
        "freq":915.000000,
        "stat":1,
        "modu":"LORA",
        "datr":"SF7BW125",
        "codr":"4/5",
        "lsnr":format(random.uniform(1,10),'.1f'),
        "rssi":random.randint(-86,-68),
        "size":64,
        "data":yowa_v(count)} 
    
    ta_encoded_json = json.dumps(ta_payload) 
    yo_encoded_json = json.dumps(yo_payload) 
    topic = "lora/rxpk"
    client.publish(topic, "%s " % ta_encoded_json)
    time.sleep(2)
    #client.publish(topic, "%s " % yo_encoded_json)
    
    count +=1    
    time.sleep(2)
    
  
