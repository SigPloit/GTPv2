'''
Created on 12 Sep 2017

@author: lia
'''
#import sys
#sys.path.append('..')
from gtp_v2_core.commons.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_core.commons.gtp_v2_information_element_base import *

class CreateSessionRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, source_ip, interface = 7, imsi = "222885500003199", 
                 mcc = "222", mnc="88", lac = 2788, rac = 1, 
                 apn="wap.tim.it", p_dns ='127.0.0.1', s_dns ="127.0.0.2", 
                 gsn="127.0.0.1", phone="393282270202", geo_type = 0, 
                 imei='3518280450609004', rat_type = 'E-UTRAN', tac = 0, 
                 ecgi = 0, sac = 0, cgi = 0, sm = 0, recovery = True):
        '''
        Constructor
        '''
        
        GTPV2MessageBase.__init__(self, t = 0x01,
                                  msg_type = GTPmessageTypeDigit['create-session-request'])
        
     
 
        self.add_ie(Imsi(imsi))
        self.add_ie(RatType(rat_type))
        fteid = FTeid(source_ip, interface)
        self.__fteid = fteid.get_teid()
        self.add_ie(fteid)
        self.add_ie(AccessPointName(apn))
        self.add_ie(BearerContext(ip = source_ip, interface = interface))
        self.add_ie(UserLocationInformation(mcc = mcc, mnc = mnc, lac = lac, 
                                            rac = rac, tac = tac, ecgi = ecgi, 
                                            sac = sac, cgi = cgi))
        self.add_ie(ServingNetwork(mcc = mcc, mnc = mnc))           
        self.add_ie(SelectionMode(selection_mode = sm))          
        self.add_ie(PDNAddressAllocation())
        self.add_ie(ApnRestriction())
        self.add_ie(AggregateMaximumBitRate())
        self.add_ie(Msisdn(msisdn=phone))
        self.add_ie(MEIdentity(imei))
        self.add_ie(ChargingCharacteristic())   
        self.add_ie(ProtocolConfigurationOptions(p_dns=p_dns, s_dns=s_dns))
        if recovery :
            self.add_ie(Recovery())
        
    
    def get_fteid(self):
        return self.__fteid
     
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
         