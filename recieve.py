import redis


r = redis.Redis(host='211.23.17.100')
pubsub = r.pubsub()
pubsub.subscribe('lorainfo')

for item in pubsub.listen():
    print item
