'''
Created on 12 Dec 2017

@author: lia
'''
#import mobility_mgmt_messages
#import other_no_3gpp_accesss_messages

from path_mgmt_messages.echo import EchoRequest, EchoResponse
from tunnel_mgmt_messages.create_session import CreateSessionRequest, CreateSessionResponse

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
                   'ies': []}
        
    def parseConfigs(self):
        confobj = ConfigObj(self.__cfg)
        
        if 'GENERIC' not in confobj.sections:
            raise ConfigObjError('Section GENERIC is required')
        
        if 'interface' not in confobj['GENERIC']:
            raise ConfigObjError('Value "GENERIC.interface" is required')
        self.__configs['interface'] = confobj['GENERIC']['interface']
        
        if 'base_message_list' not in confobj['GENERIC']:
            raise ConfigObjError('Value "GENERIC.base_message_list" is required')
        self.__configs['base_message_list'] = confobj['GENERIC']['base_message_list'].strip(" ").split(',')
        
        if '3gpp_messages_list' not in confobj['GENERIC']:
            raise ConfigObjError('Value "GENERIC.3gpp_messages_list" is required')
        self.__configs['3gpp_messages_list'] = \
            confobj['GENERIC']['3gpp_messages_list'].strip(" ").split(',')
        
        if self.__configs['base_message_list'] is None or \
            self.__configs['base_message_list'] == "" \
            or self.__configs['base_message_list'] == []:
            self.__configs['base_message_list'] = [1, 2]
        
        if not isinstance(self.__configs['base_message_list'], list):
            self.__configs['base_message_list'] = [self.__configs['base_message_list']]
            

        self.__configs['3gpp_messages_list'] = \
            confobj['GENERIC']['3gpp_messages_list'].strip(" ").split(',')            
                  
        if 'IES' not in confobj.sections:
            raise ConfigObjError('Section IEs is required')
        self.__msgs = self.__create_messages(confobj['IES'])
              
    
    def __format_base_messages(self):
        msgs = []
        for msg_type in self.__configs['base_message_list']:
            if msg_type == 1 :
                msgs.append(EchoRequest())
            elif msg_type == 2 :
                msgs.append(EchoResponse())
            else: 
                raise Exception("%s:%s - Invalid base msg type "
                                "%d"%(self.__class__.__name__, 
                                      "__format_base_messages",
                                      msg_type))
        return msgs
    
    
    def __format_interface_msg(self, confobj):
        msgs = []
        for msg_type in self.__configs['3gpp_messages_list']:
            if msg_type == 32 :
                msgs.append(CreateSessionRequest(confobj['GENERIC']['source_ip'], 
                    self.__configs['interface'], imsi = confobj['IEs']['imsi'], 
                    mcc = confobj['IEs']['mcc'], mnc = confobj['IEs']['mnc'],
                    lac = int(confobj['IEs']['lac']), rac = int(confobj['IEs']['rac']),
                    apn = confobj['IEs']['apn'], p_dns = confobj['IEs']['primary_dns'],
                    s_dns = confobj['IEs']['secondary_dns'], gsn = confobj['IEs']['gsn'],
                    phone= confobj['IEs']['msisdn'], geo_type = int(confobj['IEs']['geo_type']),
                    imei = confobj['IEs']['imei'], rat_type = confobj['IEs']['rat_type']))
            elif msg_type == 3:
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