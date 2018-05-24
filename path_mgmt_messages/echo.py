'''
Created on 20 Nov 2017

@author: lia
'''
import sys
sys.path.append('..')
from gtp_v2_core.commons.gtp_v2_msg_base import GTPV2MessageBase
from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_core.commons.gtp_v2_information_element_base import Recovery

class EchoRequest(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, version = 0x02):
        '''
        Constructor
        '''
        if version == 0x02 :
            GTPV2MessageBase.__init__(self, 
                                      msg_type = GTPmessageTypeDigit['echo-request']
                                      )
            self.add_ie(Recovery(rc = 13))
#         else :
#             GTPV1MessageBase.__init__(self, 
#                                        msg_type = GTPmessageTypeDigit['echo-request'])                   
        
        
class EchoResponse(GTPV2MessageBase):
    '''
    classdocs
    '''


    def __init__(self, seq_num, version = 0x02):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, msg_type = GTPmessageTypeDigit['echo-response'],
                                  sequence = seq_num, version = version) 
        self.add_ie(Recovery(rc = 0))         
 