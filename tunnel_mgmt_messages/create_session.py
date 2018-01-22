'''
Created on 12 Sep 2017

@author: lia
'''
from gtp_v2_base.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_base.gtp_v2_commons import *
from gtp_v2_base.gtp_v2_information_element_base import *

class CreateSessionRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, source_ip, interface, imsi = "222885500003199", mcc = "222", mnc="88", 
                lac = 2788, rac = 1, apn="wap.tim.it", p_dns ='127.0.0.1',
                s_dns ="127.0.0.2", gsn="127.0.0.1", phone="393282270202",
                geo_type = 0, imei='3518280450609004', rat_type = 'E-UTRAN'
                ):
        '''
        Constructor
        '''
        
        GTPV2MessageBase.__init__(self, t = 0x01, msg_type = GTPmessageTypeDigit['create-session-request'])
        
        self.add_ie(Imsi(imsi))
        self.add_ie(RatType(rat_type))
        self.add_ie(FTeid(source_ip, interface))
        self.add_ie(AccessPointName(apn))
        #self.add_ie(BearerContextCreateSessionRequest(ip = source_ip, 
        #                                              interface = interface))
        #self.add_ie(UserLocationInformation())
        #self.add_ie(ServingNetwork(mcc=mcc, mnc=mnc))           
        #self.add_ie(SelectionMode(0))          
        #self.add_ie(PDNAddressAllocation())
        #self.add_ie(ApnRestriction())
        #self.add_ie(AggregateMaximumBitRate())
        #self.add_ie(Msisdn(msisdn=phone))
        #self.add_ie(MEIdentity(imei))
        #self.add_ie(ChargingCharacteristic())   
        #self.add_ie(ProtocolConfigurationOptions(p_dns=p_dns, s_dns=s_dns))
        #self.add_ie(Recovery())
        

     
     
class CreateSessionResponse(GTPV2MessageBase):
    '''
    classdocs
    '''
    def __init__(self, teid, sqn, source_ip, interface):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['create-session-response'])
        self.set_teid(teid)
        self.set_sequence_number(sqn)
        self.add_ie(FTeid(source_ip, interface))
        self.add_ie(SuccessCause())
         