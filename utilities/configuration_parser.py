'''
Created on 12 Dec 2017

@author: lia
'''
import sys
sys.path.append('..')
from gtp_v2_core.path_mgmt_messages.echo import EchoRequest, EchoResponse
from gtp_v2_core.tunnel_mgmt_messages.create_session import CreateSessionRequest,\
 CreateSessionResponse

from configobj import ConfigObj, ConfigObjError

class parseConfigs(object):
    '''
    classdocs
    '''


    def __init__(self, config_file):
        '''
        Constructor
        '''
        self.__msgs = []
        if config_file is None or config_file is "":
            raise Exception("No config file provided")
        self.__cfg = config_file
        self.__configs = {'interface': None,
                   'base_message_list': [],
                   '3gpp_messages_list': [],
                   'IES': []}
        self.__parseConfigs()
        
    def __parseConfigs(self):
        confobj = ConfigObj(self.__cfg)
        
        if 'GENERIC' not in confobj.sections:
            raise ConfigObjError('Section GENERIC is required')
        
        if 'interface' not in confobj['GENERIC']:
            raise ConfigObjError('Value "GENERIC.interface" is required')
        self.__configs['interface'] = confobj['GENERIC']['interface']
        
        if 'base_message_list' not in confobj['GENERIC']:
            self.__configs['base_message_list'] = [1]
        
        self.__configs['base_message_list'] = confobj['GENERIC']['base_message_list']
        
        if '3gpp_messages_list' not in confobj['GENERIC']:
            raise ConfigObjError('Value "GENERIC.3gpp_messages_list" is required')
        self.__configs['3gpp_messages_list'] = confobj['GENERIC']['3gpp_messages_list']
        
        if self.__configs['base_message_list'] is None or \
            self.__configs['base_message_list'] == "" \
            or self.__configs['base_message_list'] == []:
            self.__configs['base_message_list'] = [1]
                      
        self.__msgs = self.__create_messages(confobj)
              
    
    def __format_base_messages(self):
        msgs = []
        for msg_type in self.__configs['base_message_list']:
            if int(msg_type) == 1 :
                msgs.append(EchoRequest())
            elif int(msg_type) == 2 :
                msgs.append(EchoResponse(1))
            else: 
                raise Exception("%s:%s - Invalid base msg type "
                                "%d"%(self.__class__.__name__, 
                                      "__format_base_messages",
                                      int(msg_type)))
        return msgs
    
    
    def __format_interface_msg(self, confobj):
        msgs = []
        if confobj is None:
            raise Exception("%s:%s - Configuration Object is None. "
                            %(self.__class__.__name__, "__format_base_messages")) 
        if 'IES' not in confobj.sections:
            raise ConfigObjError('Section IES is required')
        for msg_type in self.__configs['3gpp_messages_list']:
            if int(msg_type) == 32 :
               
                msgs.append(CreateSessionRequest(source_ip = confobj['GENERIC']['source_ip'], 
                    interface = int(self.__configs['interface']), imsi = confobj['IES']['imsi'], 
                    mcc = confobj['IES']['mcc'], mnc = confobj['IES']['mnc'],
                    lac = int(confobj['IES']['lac']), rac = int(confobj['IES']['rac']),
                    apn = confobj['IES']['apn'], p_dns = confobj['IES']['primary_dns'],
                    s_dns = confobj['IES']['secondary_dns'], gsn = confobj['IES']['gsn'],
                    phone= confobj['IES']['msisdn'], geo_type = int(confobj['IES']['geo_type']),
                    imei = confobj['IES']['imei'], rat_type = confobj['IES']['rat_type']))
                
            elif int(msg_type) == 33:
                msgs.append(int(CreateSessionResponse(confobj['GENERIC']['teid']), 
                       int(confobj['GENERIC']['sqn']), confobj['GENERIC']['source_ip'], 
                       self.__configs['interface']))
        return msgs
    
    def __create_messages(self, confobj):
        msgs = []
        if len(self.__configs['base_message_list']) > 0 :
            msgs.extend(self.__format_base_messages())
        if len(self.__configs['3gpp_messages_list']) > 0 :
            msgs.extend(self.__format_interface_msg(confobj))
        return msgs
    
    def get_unpacked_messages(self):   
        return self.__msgs