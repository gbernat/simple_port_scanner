import pytest
from src.port_scanner.main import *

# 
# shuffle_por_list
#
@pytest.mark.parametrize('port_list, shuffled_port_list',
                            [
                                ([1,2,3,4], [1,2,3,4]),
                                (['1', '2', 3, 4], ['1', '2', 3, 4]),
                                #([3, 4], [3, 4]),
                            ])
def test_shuffle_port_list(port_list, shuffled_port_list):
    assert shuffle_port_list(port_list) != shuffled_port_list
    assert len(shuffle_port_list(port_list)) == len(shuffled_port_list)

def test_shuffle_port_list_boundaries():
    assert shuffle_port_list([]) == []
    assert shuffle_port_list() == []

# 
# get_random_delays
#
def test_get_random_delays():
    assert get_random_delays('aa') == []
    assert get_random_delays() == []
    assert get_random_delays(0) == []
    assert len(get_random_delays(10)) == 10

# 
# get_stealth_port_list
#
def test_get_stealth_port_list():
    assert get_stealth_port_list() == []
    assert get_stealth_port_list('aa') == []
    assert len(get_stealth_port_list([1,2,3,4])) == 4

#
# is_web_server
#
def test_is_web_server():
    assert is_webserver() == False
    assert is_webserver(1) == False

#
# check_port
#
@pytest.mark.parametrize('destination, check_result',
                            [
                                (('',0,0), {'port': 0, 'status': 'closed', 'target': ''}),
                                (('',0), {}),
                                ((''), {}),
                                ((1), {}),
                                (None, {}),
                                (('www.google.com',80,0), {'port': 80, 'status': 'open', 'target': 'www.google.com', 'web_server': True}),
                                (('www.google.com',80,5), {'port': 80, 'status': 'open', 'target': 'www.google.com', 'web_server': True}),
                                (('www.google.com',81,0), {'port': 81, 'status': 'closed', 'target': 'www.google.com'}),
                            ])
def test_check_port(destination, check_result):
    assert check_port(destination) == check_result

#
# print_results, export_results
#
def test_output_results():
    assert print_results(1) == None
    assert print_results([]) == None
    assert export_results(1) == None
    assert export_results([]) == None

