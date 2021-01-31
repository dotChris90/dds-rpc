from idl_parser import parser

class InterfaceFormer(object):
    def __init__(self, *args):
        super(InterfaceFormer, self).__init__(*args))
        self.interfaces = []

    def parse_for_interfaces(file_path):
        



fd = open('./idls/robot_2.idl','r')

A = parser_.load(fd.read(),['idls'])
