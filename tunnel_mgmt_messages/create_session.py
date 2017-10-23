'''
Created on 12 Sep 2017

@author: lia
'''
from gtp_v2_base.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_base.gtp_v2_commons import *
from gtp_v2_base.gtp_v2_information_element_base import Imsi, RatType, FTeid,\
AccessPointName

class CreateSessionRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, source_ip, interface, imsi = "222885500003199", mcc = "222", mnc="88", 
                lac = 2788, rac = 1, apn="wap.tim.it", p_dns ='127.0.0.1',
                s_dns ="127.0.0.2", gsn="127.0.0.1", msisdn="393282270202",
                geo_type = 0, imei='3518280450609004', rat_type = 'E-UTRAN'
                ):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['create-session-request'])
        self.__ies = []
        self.__ies.append(Imsi(imsi))
        self.__ies.append(RatType(rat_type))
        self.__ies.append(FTeid(source_ip, interface))
        self.__ies.append(AccessPointName(apn))
        
     
     
class CreateSessionResponse(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, GTPmessageTypeDigit['create-session-response'])
         