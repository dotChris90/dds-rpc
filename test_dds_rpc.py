from dds_rpc import __version__
from dds_rpc import InterfaceFormer

def test_version():
    assert __version__ == '0.1.0'

def test_parser():
    if_former = InterfaceFormer.InterfaceFormer()
    if_former.parse_for_interfaces('tests/idls/robot_2.idl')
    if_former.determine_idl_each_interface()

test_parser()