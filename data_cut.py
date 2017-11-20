import base64
#class data_cut:
    
    
def yowa(decode,topic,rssi,lsnr,freq):
    typ = decode[8] + decode[9]
    idd = decode[10]
    battery = decode[22] + decode[23]
    #lat = decode[24]+decode[25]
    #lng = str(int(decode[32]+decode[33],16))
    
    x = decode[40]+decode[41]
    y = decode[44]+decode[45]
    z = decode[48]+decode[49]
    Sos = decode[52]+decode[53]
    status = decode[55]+decode[56]
    check = decode[59]+decode[60]
    for i in xrange(1,12):
        idd = idd  + decode[i+10]
       # j =i-1
       # if j%2==0 and j != 10:
       #     idd = idd + ":"
    #for i in xrange(1,7):
    #    lat = lat + decode[i+25]
    #    lng = lng + decode[i+33]
  
    lat = chr(int(decode[24]+decode[25],16))+chr(int(decode[26]+decode[27],16))+chr(int(decode[28]+decode[29],16))+chr(int(decode[30]+decode[31],16))
    lng = chr(int(decode[32]+decode[33],16))+chr(int(decode[34]+decode[35],16))+chr(int(decode[36]+decode[37],16))+chr(int(decode[38]+decode[39],16))


    if x == "2b":
        x = "+"
    elif x == "2d":
        x = "-"
    if y == "2b":
        y ="+"
    elif y == "2d":
        y = "-"
    if z == "2b":
        z = "+"
    elif z == "2d":
        z = "-"
    for i in xrange(1,3):
        x = x + decode[i+41]
        y = y + decode[i+45]
        z = z + decode[i+49]
        Sos = Sos + decode[i+53]
        status = status + decode[i+56]
        check = check + decode[i+60]
    
    
    data =[{ "node_id":idd,
             "battery":battery,#int(battery,16),
             "lng": lng ,
             "lat": lat ,
             "axis":{
                    "X": x ,
                    "Y": y ,
                    "Z": z ,
                   },
             "SoS": Sos,#int(Sos) ,
             "status": status,#int(status) ,
             "check_sum": check,#int(check) ,
             "source": topic ,
             "type": typ ,
             "gateway_id": "d8:b9:0e:00:12:21" ,
             "rssi": rssi,
             "lsnr": lsnr,
             "freq": freq
            }]
    
    return data

def taifa(code,topic,rssi,lsnr,freq): 
        
        decode = base64.b64decode(code)
#        decoded = base64.b64decode(code)
#        cry=crypto.decodePHYpayload(decoded.encode("hex"),Key)
#        decode = cry.getdata()
#        decode =decoded.split(',')
        print decode
         
        
        typ = decode[0]+decode[1]
        idd = decode[2]
        battery = decode[10]+decode[11]
        lat = decode[12]
        lng = str(int(decode[20]+decode[21],16))
        
        x = int(decode[30]+decode[31],16)/100.0
        y = int(decode[34]+decode[35],16)/100.0
        z = int(decode[38]+decode[39],16)/100.0
        
        Sos = int(decode[40]+decode[41]+decode[42]+decode[43])
        status = int(decode[44]+decode[45]+decode[46]+decode[47])
        check = int(decode[48]+decode[49]+decode[50]+decode[51])
        
        for i in xrange(1,8):
            idd = idd + decode[i+2]
            lat = lat + decode[i+12]
        for i in xrange(1,7):
            lng = lng + decode[i+21]
        
        if decode[29] == "0":
            sign = "+"
            x = sign + str(x)
        else:
            sign = "-"
            x = sign + str(x)
        if decode[33] == "0":
            sign = "+"
            y = sign + str(y)
        else:
            sign = "-"
            y = sign + str(y)
        if decode[37] == "0":
            sign = "+"
            z = sign + str(z)
        else:
            sign = "-"
            z = sign + str(z)
        
        lat = float(lat)/1000000.0        
        lng = float(lng)/1000000.0    
    
        data =[{"node_id" : idd ,
                "battery" : battery ,
                "lng" : lng ,
                "lat" : lat ,
                "axis" : {
                            "X" : x ,
                            "Y" : y ,
                            "Z" : z ,
                          },
                "SoS" : Sos ,
                "status" : status ,
                "check_sum" : check ,
                "source" : topic ,
                "type" : typ ,
                "gateway_id" : "d8:b9:0e:00:12:21" ,
                "rssi": rssi,
                "lsnr": lsnr,
                "freq": freq
                }]
        return data

def taifa1(code,topic,rssi,lsnr,freq):
    decodes = base64.b64decode(code)
    decode = decodes.encode("hex")
    typ = decode[0]+decode[1]
    idd = decode[2]
    battery = int(decode[14]+decode[15],16)
    lat = decode[16]+decode[17]#N=00 or S=01
    lng = decode[24]+decode[25]#E=00 or W=01
    x = decode[32]+decode[33]
    if x=="00":
        x="+"+str(int(decode[34]+decode[35],16)/100.0)
    else:
        x="-"+str(int(decode[34]+decode[35],16)/100.0)

    y = decode[36]+decode[37]
    if y=="00":
        y="+"+str(int(decode[38]+decode[39],16)/100.0)
    else:
        y="-"+str(int(decode[38]+decode[39],16)/100.0)

    z = decode[40]+decode[41]
    if z=="00":
        z="+"+str(int(decode[42]+decode[43],16)/100.0)
    else:
        z="-"+str(int(decode[42]+decode[43],16)/100.0)

    Sos = decode[44]+decode[45]
    status = int(decode[46]+decode[47],16)
    check = decode[48]+decode[49]
    for i in xrange(1,12):
        idd = idd + decode[i+2]
    for i in xrange(1,7):
        lat = lat + decode[i+17]
        lng = lng + decode[i+25]
    
    lat = int(lat,16)        
    lng = int(lng,16)
    print(lat,lng)  
        
    #degree 
    #str(lat/100000)
    #minute
    #str((lat%100000)*0.001)
    #second
    #str(((lat%100000)*0.001)%1*60) 

    lat=("%.6f"%(lat/100000+(((lat%100000)*0.001)/60)))
    lng=("%.6f"%(lng/100000+(((lng%100000)*0.001)/60)))

#    if status==0:
#        status="Normal"
#    elif status==1:
#        status="GPS fault"
#    elif status==2:
#        status="battery fault"
#    elif status==3:
#        status="GPS,battery fault"

    if status==4:
        status="3-axis fault"
        Sos=1
    elif status==5:
        #status="3-axis,GPS fault"
        Sos=1
    elif status==6:
        #status="3-axis,battery fault"
        Sos=1
    elif status==7:
        Sos=1
        #status="3-axis,battery,GPS fault"
    
    rssi = str(rssi)+" dBm"
    lsnr = str(lsnr)+ " dB"
    freq = str(freq)+" MHz"   


    data =[{"node_id" : idd ,
            "battery" : battery ,
            "lng" : lng ,
            "lat" : lat ,
            "axis" : {
                        "X" : x ,
                        "Y" : y ,
                        "Z" : z ,
                      },
            "SoS" : int(Sos) ,
            "status" : status ,
            "check_sum" : check ,
            "source" : topic ,
            "type" : typ ,
            "gateway_id" : "d8:b9:0e:00:12:21" ,
            "rssi": rssi,
            "lsnr": lsnr,
            "freq": freq
            }]
    return data

