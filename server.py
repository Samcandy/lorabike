import subprocess
import paho.mqtt.client as mqtt
import json
import base64
from lib import redis_mq

MQTT_PORT = 1883
MQTT_SERVER = '192.168.1.24'
MQTT_TOPIC = 'lora/rxpk'
lora_appskey = '0e5daa99a3f64375b7a00208598dc897'
lora_netskey = '7041f447fce24eadaa02d6aa82cfae1d'


def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC + '/#')


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    rssi = payload['rssi']
    lsnr = payload['lsnr']
    freq = payload['freq']
    decoding_base64 = payload['data']
    decoded = base64.b64decode(decoding_base64)
    phypayload = decoded.hex()
    mhdr = phypayload[:2]
    macpayload = phypayload[2:-8]
    mic = phypayload[-8:]
    fhdr = macpayload[:14]
    fport = macpayload[14:16]
    frmpayload = macpayload[16:]
    devaddr = fhdr[:8]
    fctrl = fhdr[8:10]
    fcnt = fhdr[-4:]
    # Reorganization DevAddr
    devaddr = devaddr[-2:] + devaddr[-4:-2] + devaddr[-6:-4] + devaddr[:-6]

    print('PHYPayload:', phypayload)
    print('PHYPayload = MHDR[1] | MACPayload[..] | MIC[4]')
    print('MHDR:', mhdr)
    print('MACPayload:', macpayload)
    print('MIC:', mic)
    print()
    print('MACPayload = FHDR | FPort | FRMPayload')
    print('FHDR:', fhdr)
    print('FPort:', fport)
    print('FRMPayload:', frmpayload)
    print()
    print('FHDR = DevAddr[4] | FCtrl[1] | FCnt[2] | FOpts[0..15]')
    print('DevAddr:', devaddr)
    print('FCtrl:', fctrl)
    print('FCnt:', fcnt)
    print('FOpts:', 'None')

    ret_code, ret = subprocess.getstatusoutput(
        'node lib/lora-packet/bin/lora-packet-decode --appkey {} --nwkkey {} --hex {}'.format(
            lora_appskey,
            lora_netskey,
            phypayload
        )
    )
    # print(ret)
    plaintext = ret[ret.find('Plaintext'):
              ret.find('( FHDR = DevAddr[4] | FCtrl[1] | FCnt[2] | FOpts[0..15] )')]
    # Reorganization Plaintext
    plaintext = plaintext.split('=')[1].split(' ')[1]
    print('Plaintext', plaintext)
    # plaintext = '0000015080D15BCE801EC5C79A07320078'
    lat = plaintext[8:16]
    lon = plaintext[16:24]
    t_lat = lat[-2:] + lat[-4:-2] + lat[-6:-4] + lat[-8:-6]
    t_lon = lon[-2:] + lon[-4:-2] + lon[-6:-4] + lon[-8:-6]
    # Reorganization Latitude, Longitude
    print('Latitude:', t_lat)
    print('Longitude:', t_lon)
    latitude_fixed = bin(int(t_lat[:2], 16))[2:][0]
    latitude_north = bin(int(t_lat[:2], 16))[2:][1]
    latitude = int(hex(int(bin(int(t_lat[:2], 16))[4:].zfill(8), 2)) + t_lat[2:], 16)
    latitude_degree = int(latitude / 10**7) + (latitude % 10**7) / 10**5 / 60
    print(latitude_degree)
    longitude_east = bin(int(t_lon[:2], 16))[2:][0]
    longitude = int(hex(int(bin(int(t_lon[:2], 16))[2:][1:].zfill(8), 2))+t_lon[2:], 16)
    longitude_degree = int(longitude / 10**7) + (longitude % 10**7) / 10**5 / 60
    print(longitude_degree)

    date = plaintext[24:30]
    t_date = int(bin(int(date[:2], 16))[2:][:-2].zfill(8), 2)
    time = int(hex(int(bin(int(date[:2], 16))[2:][-2:].zfill(4), 2)) + date[2:], 16)
    # Reorganization Latitude, Longitude
    time = "{}:{}:{}".format(int(time/10 ** 4), int(time/10 ** 2), time % 10 ** 2)
    print('Date:', t_date)
    print('Time:', time)

    battery = int(plaintext[-2:], 16) *10 + 3000
    print('Real Voltage:', battery)

    front_data = [{
        "node_id" : "070707080808",
        "battery" : battery,
        "lng" : longitude_degree,
        "lat" : latitude_degree,
        "axis" : {
                    "X" : "None",
                    "Y" : "None",
                    "Z" : "None",
                    },
        "SoS" : 0,
        "status" : 0,
        "check_sum" : mic,
        "source" : MQTT_TOPIC,
        "type" : "None",
        "gateway_id" : "d8:b9:0e:00:12:21",
        "rssi": rssi,
        "lsnr": lsnr,
        "freq": freq
    }]
    print('------------------')
    print('Front end data:', front_data)
    json_string = json.dumps(front_data)
    print(json_string)
    red = redis_mq.pool(json_string)
    red.push()


def client_thread():
    global mqtt_looping
    client_id = ""  # If broker asks client ID.
    client = mqtt.Client(client_id=client_id)

    # If broker asks user/password.
    user = ""
    password = ""
    client.username_pw_set(user, password)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_SERVER, MQTT_PORT)
    except ConnectionRefusedError:
        print("MQTT Broker is not online. Connect later.")

    mqtt_looping = True
    print("Looping...")
    while mqtt_looping:
        client.loop()
    client.disconnect()


if __name__ == '__main__':
    client_thread()
    print("exit program")
