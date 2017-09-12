from pymongo import MongoClient
client = MongoClient('localhost', 27017)
import pprint
import time
db = client['lora-server']
count = 0
for post in db.sensor.find():
    pprint.pprint(post)
    count +=1


#for post in db.sensor.find():
#    print "lat :",post["yuwa_device"][0]["lat"],"lan :",post["yuwa_device"][0]["lng"]
#    count +=1

print "Data count: ",count

