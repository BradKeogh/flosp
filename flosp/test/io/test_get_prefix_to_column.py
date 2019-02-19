from flosp.io import get_prefix_to_column

def test_IP_default_inputs():
    assert get_prefix_to_column('ADM_DTTM') == 'ADM'
    assert get_prefix_to_column('DIS_DTTM') == 'DIS'

def test_ED_default_inputs():
    assert get_prefix_to_column('ARRIVAL_DTTM') == 'ARRIVAL'
    assert get_prefix_to_column('DEPARTURE_DTTM') == 'DEPARTURE'

def test_other_words():
    "different inputs would never be expected to those above, but for interest "
    assert get_prefix_to_column('arrival_dttm') == 'arrival'
    assert get_prefix_to_column('test_test1_test2') == 'test'