import MySQLdb

def get(commit):
    try:
        device = []        
        db = MySQLdb.connect("211.23.17.100",'root','imacwebteammysql9457songyy','lorabike')

        cursor = db.cursor()
        cursor.execute(commit)

        results = cursor.fetchall()
        
        for record in results:
            #col1 = record[0]
            #col2 = record[1]
            col3 = str(record[2])
            #col4 = record[3]
            col5 = str(record[4])
            #col6 = record[5]
            device.append(col3)
            device.append(col5)
        print device[len(device)-1]    
        #for i in xrange(1,len(device),2):
            
                    
        #return device
        db.close()
    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])


get('select * from lora_devices')

