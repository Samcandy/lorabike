import redis,sys,json,time
import paho.mqtt.client as mqtt

class pool:
    def __init__(self,data):
        self.data = data
        sys.stdout.write("\033[1;36m")
        print 
        print "Will redis push",type(self.data) 
    def push(self):
        pool = redis.ConnectionPool(host='211.20.7.119', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        r.publish('lorainfo',self.data)
        print "redis push data: ",self.data
        
        sys.stdout.write("\033[0;0m")

def sub():    
    while 1:
        r = redis.Redis(host='211.20.7.119')
        pubsub = r.pubsub()
        pubsub.subscribe('loragateway')
        for item in pubsub.listen():
            #print item
            if type(item['data']) == str:
                data = eval(item['data'])
                gid = data['gateway_id']
                gsorce = data['gateway_sorce']
                gip = data['gateway_ip']
                lid = data['lora_id']     
                mq_publish(gsorce,gip,lid)
                break

def mq_publish(gsorce,gip,lid):
    client_id = ""
    client = mqtt.Client(client_id=client_id)
    user = ""
    password = ""
    client.username_pw_set(user, password)
    client.connect(gip)

    topic = "lora/"+gsorce
    payload = lid
    client.publish(topic,payload)
    sys.stdout.write("\033[1;92m")
    print "publish Gateway By MQTT"
