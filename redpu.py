import redis

r = redis.Redis(host='211.20.7.119')
a={"gateway_sorce":"txdw","gateway_id":"d8:b9:0e:00:12:21","gateway_ip":"10.21.20.120","lora_id":"a1b2c3d4e5f6"}
r.publish('loragateway', a)

