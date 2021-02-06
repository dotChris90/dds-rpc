from idl_parser import parser
from idl_parser import interface
from pathlib import Path
class InterfaceFormer(object):

    def __init__(self, *args):
        super(InterfaceFormer, self).__init__(*args)
        self.interfaces = []

    def _get_interfaces(self,module):
        if_return = []
        if (module.interfaces == []):
            pass 
        else:
            for interface in module.interfaces:
                if_return.append(interface)
        if (module.modules == []):
            pass 
        else:
            for module_idx in module.modules:
                if_return_idx = self._get_interfaces(module_idx)
                if (if_return_idx == []):
                    pass 
                else: 
                    for idx in if_return_idx:
                        if_return.append(idx)
        return if_return

    def parse_for_interfaces(self,file_path : str):
        file = Path(file_path)
        file_path = str(file.absolute())
        # fd = file descriptor
        with open(file_path,'r') as fd:
            file_content = fd.read()
            parser_obj = parser.IDLParser()
            directories = []
            directory = str(file.parent.absolute())
            directories.append(directory)
            idl_obj = parser_obj.load(file_content,directories)
            modules = idl_obj.modules
            for module in modules:
                if_ = self._get_interfaces(module)
                for if_idx in if_:
                    self.interfaces.append(if_idx)
                
    def determine_idl_each_interface(self):
        messages_in_out  = {}
        for interface in self.interfaces:
            if_name = interface.name
            for if_method in interface.methods:
                if_method_name = if_method.name 
                msg_in_name     = if_name + '_' + if_method_name + '_in'
                msg_out_name    = if_name + '_' + if_method_name + '_out'
                messages_in_out[msg_in_name]  = []
                messages_in_out[msg_out_name] = []
                for argument in if_method.arguments:
                    arg = {}
                    arg['name']         = argument.name
                    if (argument.type.classname == 'IDLPrimitive'):
                        arg['type']     = argument.type.basename
                    else:
                        arg['type']     = argument.type.name
                    if (argument.direction == 'out'):
                        messages_in_out[msg_out_name].append(arg)    
                    else:
                        messages_in_out[msg_in_name].append(arg)
                if (messages_in_out[msg_in_name] == []):
                    arg = {}
                    arg['name'] = 'dummy'
                    arg['type'] = 'dds::rpc::UnusedMember'
                    messages_in_out[msg_in_name] = arg
                else:
                    pass 
                if (messages_in_out[msg_out_name] == []):
                    arg = {}
                    arg['name'] = 'dummy'
                    arg['type'] = 'dds::rpc::UnusedMember'
                    messages_in_out[msg_out_name] = arg
                else:
                    pass 
        return messages_in_out