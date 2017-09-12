from Crypto.Cipher import AES
import binascii
class decodePHYpayload:
    def __init__(self, PHYpayload, key):
        """
        name       type    
        PHYpayload str 
        key        str   
        """
        #total 35 bytes
        print PHYpayload
        print "PHYpayload len :{}".format(len(PHYpayload))
        self.addr = PHYpayload[2:10]    #4 bytes
        self.FCnt = PHYpayload[12:16]   #2 bytes
        self.data = PHYpayload[18:-8]    
        self.MIC = PHYpayload[-8:]      #4 bytes
        self.appkey = binascii.unhexlify(key) #16 bytes
        
        Ablock = "01"+"00000000" + "00" + self.addr + self.FCnt + "0000" + "000"
        self.Ablock = Ablock
    
    def getdata(self):
        """
        get_data return data(type str)
        """
        en = AES.new(self.appkey, AES.MODE_ECB) #create the ECB mode
        s = ""
        b_enA = ""
        b_enA1 = ""
        hex_data = binascii.unhexlify(self.data)#transform to hex
        b_data = bytearray(hex_data)            #datatype transform to bytearray
        len_l6 = 0
        len_16 = len(b_data)/16
            
        for i in range(1,len_16+2):
            Ablock = "01"+"00000000" + "00" + self.addr + self.FCnt + "0000" + "000" +str(i)
            print "Ablock  :{}".format(Ablock)
            hex_Ablock = binascii.unhexlify(Ablock) #transform to hex
            enA = en.encrypt(hex_Ablock)            #encrypt the ECB mode
            b_enA = bytearray(enA)                  #datatype transform to bytearray
            print "Ablock encrypt  :{}".format(enA.encode("hex"))
            b_enA1 = b_enA1 + b_enA
            
        
        print "data_len {}".format(len(b_data))
        #b_enA = b_enA + b_enA1
           
        s = str(b_data[0] ^ b_enA1[0])    
        for i in range(len(b_data)-1):
            s =s+","+ str(b_data[i+1] ^ b_enA1[i+1])#[2:]
        return s
#x=decodePHYpayload('407856341280584164CEC7274788522A478E47C7D83059B60631A402BA4CD7274BF2C4','2b7e151628aed2a6abf7158809cf4f3c')
#print x.getdata()
