'''
Created on 12 Sep 2017

@author: lia
'''
import random
import struct

from IPy import IP
import gtp_v2_commons 

'''
    8     7     6     5     4     3     2     1    Octets
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Type = xxx (decimal)          |   1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 IE Length (n)                 |  2-3
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Spare           |    Instance           |  4
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                IE Specific data or content    | 5-(5+n)
|                    of grouped IE              |
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

'''
      
        
class InformationElementBase(object):
    '''
    Virtual base class for an information element
    '''

    def __init__(self, ie_type):
        '''
        Constructor
        '''
        if not isinstance(ie_type, int) :
            raise TypeError('Invalid IE Type %s.Expected int.'%(str(type(ie_type))))
        if self.__is_reserved(ie_type) :
            raise Exception("Invalid IE Type")
        self.__ie_type = ie_type
        self.__len = 0 #the length of the TLI fields shall not be included
        self.__instance = 0x00
        self.__spare = 0x00
    
    def __is_reserved(self, ie_type):
        
        if ie_type in gtp_v2_commons.RESERVED_IE_TYPES:
            return True
        return False
    
    def __get_packed_hdr(self):
        hdr = struct.pack("!B", self.__ie_type)
        hdr += struct.pack("!H", self.__len)
        other_data = (self.__spare << 4) + (self.__instance & 15)
        hdr += struct.pack("!B", other_data)
        return hdr        
    
    def __get_val(self):
        pass
    
    def get_packed_ie(self):
        return (self.__get_packed_hdr() + self.__get_val())
    
    def get_total_len(self):
        return self.__len + 4

class UserLocationInformation(InformationElementBase) :
    def __init__(self, mcc = "222", mnc = "01", lac = 0x00, sac = 0x00, 
                 tac = 0x00, rac = 0x00, cgi = 0x00, ecgi = 0x00):
        InformationElementBase.__init__(self, 86)
        self.__len = 0
        mni = gtp_v2_commons.MobileNetworkIdentifier(mcc, mnc)
        self.__lai = self.__sai = self.__tai = self.__rai = self.__cgi = \
        self.__ecgi = None
        self.__flags = 0x00
        if lac :
            self.__lai = gtp_v2_commons.AI(mni, lac)
            self.__len += 5
            self.__flags = (self.__flags | (1 << 5))
            if sac :
                self.__sai = gtp_v2_commons.LocationInformation(self.__lai, sac)
                self.__len += 7
                self.__flags = (self.__flags | (1 << 1))
            if rac :
                self.__rai = gtp_v2_commons.LocationInformation(self.__lai, rac)
                self.__len += 7
                self.__flags = (self.__flags | (1 << 2))
            if cgi :
                self.__cgi = gtp_v2_commons.LocationInformation(self.__lai, cgi)
                self.__len += 7
                self.__flags = (self.__flags | 1)                
        if tac :
            self.__tai = gtp_v2_commons.AI(tac)    
            self.__len += 5
            self.__flags = (self.__flags | (1 << 3))
        if ecgi:
            self.__ecgi = gtp_v2_commons.ECGI(mni, ecgi)
            self.__len += 7
            self.__flags = (self.__flags | (1 << 4))
    
    def __get_val(self):      
        out = struct.pack("!B", self.__flags)
        if self.__cgi :
            out += self.__cgi.get_packed_val() 
        if self.__sai :
            out += self.__sai.get_packed_val()
        if self.__rai :
            out += self.__rai.get_packed_val()
        if self.__tai :
            out += self.__tai.get_packed_val()
        if self.__ecgi :
            out += self.__ecgi.get_packed_val()
        return out  
   
    
    
class Imsi (InformationElementBase):    
    
    def __init__(self, imsi = "222015500003199") :
        InformationElementBase.__init__(self, 2)
        if len(imsi) != 15 :
            raise Exception("invalid imsi length %d"%(len(imsi))) 
        self.__val =  imsi
        self.__len = 8
    
    def __get_val(self):

        i = 0
        hex_imsi = ''
        while i < 13 :
            c1 = self.__val[i]
            c2 = self.__val[i+1]
            self.__val += c2
            hex_imsi+=c1
            i += 2
        hex_imsi += ("f" + self.__val[14])
        
        if gtp_v2_commons.DEBUG :
            print "imsi :", self.__val
            print "hex imsi:", hex_imsi
        return bytearray.fromhex(hex_imsi)
    

class Msisdn(InformationElementBase):
    def __init__(self, msisdn="393356534399"):
        InformationElementBase.__init__(self, 134)
        self.__val = str(msisdn)
        self.__len = 6

        
    def __get_val(self):
        length = len(self.__val)
        to_append = ''
        if length % 2 != 0 :
            length = length - 1
            to_append = 'f' + self.__val[length]
        hex_val = ''
        i = 0
        while i < (length - 1) :
            c1 = self.__val[i]
            c2 = self.__val[i+1]
            hex_val += c2
            hex_val +=c1
            i += 2
        hex_val += to_append
        return bytearray.fromhex(hex_val)
    
class ApnRestriction(InformationElementBase):
    
    def __init__(self, val = 0):
        if val < 0 or val > 5 :
            raise Exception("invalid apn restriction value %d"%(val))
        InformationElementBase.__init__(self, 149)
        self.__len = 1    # 2 bytes
        self.__val = val # 1 byte
    
    def __get_val(self):
        return struct.pack("!B", self.__val)

class RatType(InformationElementBase):
    # expected values:
    # 1 UTRAN
    # 2 GERAN
    # 3 WLAN
    # 4 GAN
    # 5 HSPA Evolution
    # 6 E-UTRAN
    # Other values out of scope
    # 0 reserved    
    # 7-255 spare    
    def __init__(self, rat_type = 'E-UTRAN'):
        InformationElementBase.__init__(self, 151)
        self.__len = 1 # 2 bytes
        if not gtp_v2_commons.RATTypeDigit.has_key(rat_type) :
            raise Exception("invalid rat type: %d"%(rat_type))
        self.__val = gtp_v2_commons.RATTypeDigit[rat_type] #1 byte
        
    def __get_val(self):
        return struct.pack("!B", self.__val)
    
class AccessPointName(InformationElementBase):
    def __init__(self, apn = "ggsn3.tilab.it") :
        InformationElementBase.__init__(self, 131)      
        self.__len= len(apn)# 2 bytes
        self.__val = apn
        
    def __get_val(self):
        return self.__val      
    
class MEIdentity(InformationElementBase) :
    def __init__(self, imei = "3518280450609004") :
        if len(imei) != 16 :
            raise Exception("invalid imei length %d"%len(imei)) 
        InformationElementBase.__init__(self, 154)           
        self.__len = 8    #2 bytes
        self.__val = imei # 8 bytes
            
    def __get_val(self):
        i = 0
        hex_imei=''
        while i < 15 :
            c1 = self.__val [i]
            c2 = self.__val [i+1]
            hex_imei+= c2
            hex_imei+=c1
            i += 2
        if gtp_v2_commons.DEBUG:
            print "imei:", self.__val 
            print "hex imei:", hex_imei
        return bytearray.fromhex(hex_imei)   

class ServingNetwork(InformationElementBase):
    def __init__(self, mcc = "222", mnc = "01"):
        InformationElementBase.__init__(self, 83)
        self.__len = 3
        self.__val = gtp_v2_commons.MobileNetworkIdentifier(mcc, mnc)    
        
    def __get_val(self):
        return self.__val.get_packed_val()

class FTeid(InformationElementBase):
    def __init__(self, sender_ip, interface = 10):
        if interface > 37 :
            raise Exception('Invalid 3gpp interface %d'%(interface))

        InformationElementBase.__init__(self, 87)
        self.__len = 9
        self.__ip = int(IP(sender_ip).strHex(), 16) #4 bytes
        self.__3gpp_interface = interface 
        
        self.__ip_ver_flag = (1 << 8)

        self.__teid = random.getrandbits(32)
    
    def __get_val(self):
        
        return struct.pack("!BLL", (self.__ip_ver_flag & self.__3gpp_interface),
                           self.__teid, self.__ip) 

class SelectionMode(InformationElementBase):
    def __init__(self, sm = 0):
        InformationElementBase.__init__(self, 128)
        if sm < 0 or sm > 2 :
            raise Exception("invalid Selection Mode %d"%(sm)) 
        self,__len = 1
        self.__val = sm
     
    def __get_val(self):
        return struct.pack("!B", self.__val)    
        
class Recovery(InformationElementBase):
    def __init__(self, rc = 0):
        InformationElementBase.__init__(self, 3)
        self.__len = 1 # 1 byte
        self.__val = rc
    
    def __get_val(self):
        return struct.pack("!B", self.__val)
        
class UETimeZone:
    def __init__(self):
        InformationElementBase.__init__(self, 114)
        self.__len = 2 # 2 byte
        self.__tz = 128 #1 byte
        self.__dl = 1 # 1 byte
    
    def __get_val(self):
        return struct.pack("!BB", self.__tz, self.__dl)

class ChargingCharacteristic(InformationElementBase):
    def __init__(self, cc = 0x00):
        InformationElementBase.__init__(self, 95)
        self.__len = 2
        self.__val = cc
    
    def __get_val(self):
        return struct.pack("!H", self.__val)

class AggregateMaximumBitRate(InformationElementBase):
    def __init__(self, uplink = 50000, downlink = 150000):
        InformationElementBase.__init__(self, 72)
        self.__len = 8
        self.__ambr_up = uplink
        self.__ambr_down = downlink
    
    def __get_val(self):
        return struct.pack("!LL", self.__ambr_up, self.__ambr_down)

class PDNAddressAllocation(InformationElementBase):
    def __init__(self, pdn_type = 1, ip = '0.0.0.0'):          
        if pdn_type == 1:
            self.__len = 5
            self.__ip = int(IP(ip).strHex(), 16)
        elif pdn_type == 2:
            self.__len = 18
            self.__ip = bytearray.fromhex(IP(ip).strHex())
        elif pdn_type == 3:
            self.__len = 22
            self.__ip = bytearray.fromhex(IP(ip).strHex())
        else:
            raise Exception('Invalid PDN Type %d'%(pdn_type))
        self.__pdn_type = pdn_type
        
    def __get_val(self):
        if self.__len == 5:
            return struct.pack('!BL', self.__pdn_type, self.__ip)
        return struct.pack('!B', self.__pdn_type) +  self.__ip              

            
class EPSBearerID(InformationElementBase):
    def __init__(self, ebi = 6):
        if ebi >= 1 and ebi < 5 :
            raise Exception("invalid EBI %d"%(ebi))
        self.__len = 1
        self.__val = ebi
        
    def __get_val(self):
        return struct.pack("!B", self.__val)


class BearerQoS(InformationElementBase):
    def __init__(self, pci = 0x01, pl = 0x02, pvi = 0x00, qci = 0x07, 
                 mbr_up = "0x0000000000", mbr_down = "0x0000000000", 
                 gbr_up = "0x0000000000", gbr_down = "0x0000000000"):
        InformationElementBase.__init__(self, 80)
        self.__len = 22
        self.__flags = (pci <<  7) or (pl << 5) or pvi
        self.__qci = qci
        self.__mbr_up = mbr_up
        self.__mbr_down = mbr_down
        self.__gbr_up = gbr_up
        self.__gbr_down = gbr_down
    
    def __get_val(self):
        return (struct.pack("!BB") + bytearray.fromhex(self.__mbr_up) +
                bytearray.fromhex(self.__mbr_down) + 
                bytearray.fromhex(self.__gbr_up) + 
                bytearray.fromhex(self.__gbr_down))
        
class BearerContextCreateSessionRequest(InformationElementBase):
    def __init__(self, ip, ebi = 6, pci = 0x01, pl = 0x02, pvi = 0x00, qci = 0x07, 
                 mbr_up = "0x0000000000", mbr_down = "0x0000000000", 
                 gbr_up = "0x0000000000", gbr_down = "0x0000000000",
                 interface = 10):
        InformationElementBase.__init__(self, 93)
        self.__ebi = EPSBearerID(ebi)
        self.__teid = FTeid(ip, interface)
        self.__bqos = BearerQoS(pci, pl, pvi, pci, mbr_up, mbr_down, gbr_up, 
                                gbr_down)
        self.__len = self.__ebi.get_total_len() + self.__bqos.get_total_len() +\
                    self.__teid.get_total_len()
    
    def __get_val(self):
        return (self.__ebi.get_packed_ie() + self.__bqos.get_packed_ie() + 
                self.__teid.get_packed_ie())
        
        
      
class ProtocolConfigurationOptions(InformationElementBase):
    def __init__(self, p_dns = '0.0.0.0', s_dns = '0.0.0.0', pwd = None, 
                 peer_id = None):
        InformationElementBase.__init__(self, 78)
        self.__octet_three = 0x80
        self.__proto = []
    
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'PAP', 
                        data = gtp_v2_commons.PAPData(pwd, peer_id)))
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'IPCP', 
                        data = gtp_v2_commons.IPCPData(p_dns, s_dns)))
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'DNSIPV4'))
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'IPNAS'))
        self.__len = 0
        for i in self.__proto :
            self.__len += i.get_lenght()
        
    
    def __get_val(self):
        out = struct.pack(("!B"), self.__octet_three)
        for i in self.__proto:
            out += i.get_packed()
        return out

